from typing import Callable, List

from requests import Response

from domino_cli.core.cli.Logging import error, info
from domino_cli.core.cli.RuntimeHelper import RuntimeHelper
from domino_cli.core.client.DominoClient import DominoClient
from domino_cli.core.domain.DominoCommand import DominoCommand
from domino_cli.core.domain.DominoRequest import DominoRequest


class SecretService:
    """
    Service implementation for secret management operations.
    """
    def __init__(self, domino_client: DominoClient):
        self._domino_client = domino_client

    def create_secret(self, key: str, context: str, value: str) -> None:
        """
        Creates a new secret.

        :param key: key of the secret
        :param context: context (group) of the secret
        :param value: value of the secret
        """
        request_body = {
            "key": key,
            "context": context,
            "value": value
        }

        response = self._send_command(DominoCommand.CREATE_SECRET, body=request_body)
        self._handle_response(response)

    def get_all_metadata(self) -> None:
        """
        Displays metadata of all existing secrets.
        """
        response = self._send_command(DominoCommand.RETRIEVE_ALL_METADATA)
        self._handle_response(response, self._handle_all_metadata_response)

    def get_metadata_by_key(self, key: str) -> None:
        """
        Displays metadata of the given secret.

        :param key: key of the secret to show the metadata of
        """
        response = self._send_command(DominoCommand.RETRIEVE_SECRET_METADATA, key)
        self._handle_response(response, self._handle_flat_response)

    def retrieve_secret_by_key(self, key: str) -> None:
        """
        Displays the value of the given secret.

        :param key: key of the secret to show the value of
        """
        response = self._send_command(DominoCommand.RETRIEVE_SECRET, key)
        self._handle_response(response, self._handle_flat_response)

    def retrieve_secrets_by_context(self, context: str) -> None:
        """
        Displays the value of the secrets under the given context.

        :param context: context of the secrets to show the value of
        """
        response = self._send_command(DominoCommand.RETRIEVE_SECRETS_BY_CONTEXT, context)
        self._handle_response(response, self._handle_flat_response)

    def lock_secret(self, key: str) -> None:
        """
        Locks (disables retrieval) of the given secret.

        :param key: key of the secret to lock
        """
        response = self._send_command(DominoCommand.LOCK_SECRET, key)
        self._handle_response(response)

    def unlock_secret(self, key: str) -> None:
        """
        Unlocks (enables retrieval) of the given secret.

        :param key: key of the secret to unlock
        """
        response = self._send_command(DominoCommand.UNLOCK_SECRET, key)
        self._handle_response(response)

    def delete_secret(self, key: str) -> None:
        """
        Deletes the given secret.

        :param key: key of the secret to delete
        """
        response = self._send_command(DominoCommand.DELETE_SECRET, key)
        self._handle_response(response)

    def _send_command(self, command: DominoCommand, path_variable: str | None = None, body: dict | None = None) -> Response | None:

        request = DominoRequest(
            method=command.value.method,
            path=command.value.path_template.format(path_variable),
            body=body,
            authenticated=True
        )

        try:
            return self._domino_client.send_command(request)

        except Exception as exc:
            error("Failed to execute HTTP request {0} - reason: {1}".format(request, str(exc)))
            RuntimeHelper.exit_with_error_in_cicd_mode()
            return None

    def _handle_response(self, response: Response | None, handler: Callable[[dict | List | object], None] = None) -> None:

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

    @staticmethod
    def _handle_all_metadata_response(data: List[dict]) -> None:

        for context in data:
            info(f"Secrets in context [{context["context"]}]")
            for secret in context["secrets"]:
                info("{:>30}: {}".format(secret["key"], "Retrievable" if secret["retrievable"] else "Not retrievable"))
            print()

    @staticmethod
    def _handle_flat_response(data: dict) -> None:

        if RuntimeHelper.is_cicd_mode():
            [print(f"{field}={data[field]}") for field in data]
        else:
            [info("{:>30}: {}".format(field, data[field])) for field in data]

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
