from requests import Response

from core.client.DominoClient import DominoClient
from core.domain.DominoCommand import DominoCommand
from core.domain.DominoCommand import DominoRequestDescriptor
from core.domain.DominoRequest import DominoRequest


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

        print("Sending {0} command for application {1} via Domino".format(domino_command, application))

        try:
            response: Response = self._domino_client.send_command(domino_request)

            if DominoService._is_successful(response):
                print("Command {0} successfully executed on application {1}".format(domino_command, application))
            else:
                print("Failed to execute command {0} on application {1}".format(domino_command, application))

        except Exception as exc:
            print("Failed to execute command of {0} - reason {1}".format(domino_request, str(exc)))

    @staticmethod
    def _is_successful(response: Response) -> bool:
        return 200 <= response.status_code < 300
