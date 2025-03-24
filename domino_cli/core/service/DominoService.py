from requests import Response

from domino_cli.core.cli.Logging import info, error
from domino_cli.core.cli.RuntimeHelper import RuntimeHelper
from domino_cli.core.client.DominoClient import DominoClient
from domino_cli.core.domain.DominoCommand import DominoCommand
from domino_cli.core.domain.DominoCommand import DominoRequestDescriptor
from domino_cli.core.domain.DominoRequest import DominoRequest


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

            if DominoService._is_successful(response):
                info("Command {0} successfully executed on application {1}".format(domino_command.name, application))
            else:
                error("Failed to execute command {0} on application {1} - Domino responded with {2}"
                      .format(domino_command.name, application, response.status_code))
                RuntimeHelper.exit_with_error_in_cicd_mode()

            DominoService._render_response(response)

        except Exception as exc:
            error("Failed to execute HTTP request {0} - reason {1}".format(domino_request, str(exc)))
            RuntimeHelper.exit_with_error_in_cicd_mode()

    @staticmethod
    def _is_successful(response: Response) -> bool:
        return 200 <= response.status_code < 300

    @staticmethod
    def _render_response(response: Response):
        response_dict = response.json()
        info(" --- Response details ---")
        [info("{:>20}: {}".format(field, response_dict[field])) for field in response_dict]
        print()
