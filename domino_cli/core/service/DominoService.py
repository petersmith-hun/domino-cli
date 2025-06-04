from requests import Response

from domino_cli.core.cli.Logging import info, error
from domino_cli.core.cli.RuntimeHelper import RuntimeHelper
from domino_cli.core.client.DominoClient import DominoClient
from domino_cli.core.domain.DominoCommand import DominoCommand
from domino_cli.core.domain.DominoCommand import DominoRequestDescriptor
from domino_cli.core.domain.DominoRequest import DominoRequest
from domino_cli.core.util.ResponseUtils import is_successful, render_response


class DominoService:
    """
    Service implementation handling command processing.
    """
    def __init__(self, domino_client: DominoClient):
        self._domino_client = domino_client

    def execute_lifecycle_command(self, domino_command: DominoCommand, application: str, version: str = None) -> None:
        """
        Executes the given lifecycle command for the given application.

        :param domino_command: DominoCommand object specifying the command to be executed
        :param application: application name to send the command to
        :param version: optional version number
        """
        domino_request_descriptor: DominoRequestDescriptor = domino_command.value
        formatted_path = domino_request_descriptor.path_template.format(application, version)
        domino_request = DominoRequest(domino_request_descriptor.method, formatted_path, authenticated=True)

        info("Sending {0} command for application {1} via Domino".format(domino_command.name, application))

        try:
            response: Response = self._domino_client.send_command(domino_request)

            if is_successful(response):
                info("Command {0} successfully executed on application {1}".format(domino_command.name, application))
            else:
                error("Failed to execute command {0} on application {1} - Domino responded with {2}"
                      .format(domino_command.name, application, response.status_code))
                RuntimeHelper.exit_with_error_in_cicd_mode()

            render_response(response)

        except Exception as exc:
            error("Failed to execute HTTP request {0} - reason: {1}".format(domino_request, str(exc)))
            RuntimeHelper.exit_with_error_in_cicd_mode()

    def import_definition(self, optional_definition_path: str | None = None) -> None:
        """
        Imports the given deployment definition. If path is not provided, defaults to ".domino/deployment.yml".

        :param optional_definition_path: optional path to a deployment definition
        """
        definition_path = optional_definition_path \
            if optional_definition_path \
            else ".domino/deployment.yml"
        info(f"Requesting Domino to import deployment definition from={definition_path}")

        try:

            with open(definition_path, "r") as definition_file:
                definition = definition_file.read()
                domino_request_descriptor: DominoRequestDescriptor = DominoCommand.IMPORT.value
                domino_request = DominoRequest(domino_request_descriptor.method, domino_request_descriptor.path_template,
                                               body=definition, authenticated=True, as_text=True)
                response = self._domino_client.send_command(domino_request)

                if is_successful(response):
                    info(f"Successfully imported definition {definition_path}")
                else:
                    error(f"Failed to import deployment definition {definition_path} - Domino responded with {response.status_code}")
                    RuntimeHelper.exit_with_error_in_cicd_mode()

            render_response(response)

        except Exception as exc:
            error("Failed to import definition from {0} - reason: {1}".format(definition_path, str(exc)))
            RuntimeHelper.exit_with_error_in_cicd_mode()
