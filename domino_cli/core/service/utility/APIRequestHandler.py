from typing import Callable, List, Any

from requests import Response

from domino_cli.core.cli.Logging import error, info
from domino_cli.core.cli.RuntimeHelper import RuntimeHelper
from domino_cli.core.client.DominoClient import DominoClient
from domino_cli.core.domain.CustomExceptions import ValidationException, DominoServiceException
from domino_cli.core.domain.DominoCommand import DominoCommand
from domino_cli.core.domain.DominoRequest import DominoRequest


class APIRequestHandler:
    """
    TODO.
    """
    def __init__(self, domino_client: DominoClient):
        self._domino_client = domino_client

    def send_command(self, command: DominoCommand, path_variable: str | None = None, body: dict | None = None) -> Response | None:
        """
        TODO.
        :param command:
        :param path_variable:
        :param body:
        :return:
        """
        request = DominoRequest(
            method=command.value.method,
            path=command.value.path_template.format(path_variable),
            body=body,
            authenticated=True
        )

        try:
            return self._domino_client.send_command(request)

        except Exception as exc: # TODO should refactor this one as well, return should never be "none"
            error("Failed to execute HTTP request {0} - reason: {1}".format(request, str(exc)))
            RuntimeHelper.exit_with_error_in_cicd_mode()
            return None

    def handle_response(self, response: Response | None, handler: Callable[[dict | List[dict] | object], None] | None = None) -> None:
        """
        TODO.
        :param response:
        :param handler:
        :return:
        """
        if response is None:
            return

        if response.status_code >= 300:
            error(f"Failed to execute operation, Domino responded with status {response.status_code}: {self._try_extract_message(response)}")

            if response.status_code == 400:
                self._try_render_violations(response)

        elif len(response.content) == 0:
            info("Operation finished successfully")

        elif handler is not None:
            handler(response.json())

    def handle_response_new[T](self, response: Response, mapper: Callable[[Any], T] | None = None) -> T | None:

        # TODO calling this crashes the application if session is not yet open

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
