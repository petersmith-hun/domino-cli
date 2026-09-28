from typing import Callable, Any

from requests import Response

from domino_cli.core.cli.Logging import error
from domino_cli.core.client.DominoClient import DominoClient
from domino_cli.core.domain.CustomExceptions import ValidationException, DominoServiceException
from domino_cli.core.domain.DominoCommand import DominoCommand
from domino_cli.core.domain.DominoRequest import DominoRequest


class APIRequestHandler:
    """
    Convenience wrapper class for handling API requests.
    """
    def __init__(self, domino_client: DominoClient):
        self._domino_client = domino_client

    def send_command(self, command: DominoCommand, path_variable: str | None = None, body: dict | None = None) -> Response:
        """
        Creates and sends a request to Domino.
        :param command: DominoCommand identifying the command to be executed
        :param path_variable: variables to be substituted in the path template
        :param body: request body content
        :return: raw Response
        """
        request = DominoRequest(
            method=command.value.method,
            path=command.value.path_template.format(path_variable),
            body=body,
            authenticated=True
        )

        return self._domino_client.send_command(request)

    @staticmethod
    def handle_response(response: Response, mapper: Callable[[Any], Any] | None = None) -> Any:
        """
        Handles the response from Domino.
        :param response: raw response from Domino
        :param mapper: optional mapper to be applied to the response; returns data as is if None
        :return: data transformed by the mapper or raw response if mapper is None
        """

        if response.status_code == 400:
            raise ValidationException(response)

        if response.status_code >= 300:
            raise DominoServiceException(response)

        if len(response.content) == 0:
            return None

        try:
            if mapper is None:
                mapper = lambda data: data

            return mapper(response.json())

        except:
            return response.text

    @staticmethod
    def _try_extract_message(response: Response) -> str:

        try:
            return response.json()["message"]
        except:
            return response.text

    @staticmethod
    def _try_render_violations(response: Response) -> None:

        try:
            [error(f"Invalid field [{violation["field"]}]: {violation["message"]}") for violation in response.json()["violations"]]
        except:
            pass
