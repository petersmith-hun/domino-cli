from typing import List

from domino_cli.core.cli.Logging import info
from domino_cli.core.cli.RuntimeHelper import RuntimeHelper
from domino_cli.core.domain.DominoCommand import DominoCommand
from domino_cli.core.service.utility.APIRequestHandler import APIRequestHandler


class SecretService:
    """
    Service implementation for secret management operations.
    """
    def __init__(self, api_request_handler: APIRequestHandler):
        self._api_request_handler = api_request_handler

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

        response = self._api_request_handler.send_command(DominoCommand.CREATE_SECRET, body=request_body)
        self._api_request_handler.handle_response(response)

    def get_all_metadata(self) -> None:
        """
        Displays metadata of all existing secrets.
        """
        response = self._api_request_handler.send_command(DominoCommand.RETRIEVE_ALL_METADATA)
        self._api_request_handler.handle_response(response, self._handle_all_metadata_response)

    def get_metadata_by_key(self, key: str) -> None:
        """
        Displays metadata of the given secret.

        :param key: key of the secret to show the metadata of
        """
        response = self._api_request_handler.send_command(DominoCommand.RETRIEVE_SECRET_METADATA, key)
        self._api_request_handler.handle_response(response, self._handle_flat_response)

    def retrieve_secret_by_key(self, key: str) -> None:
        """
        Displays the value of the given secret.

        :param key: key of the secret to show the value of
        """
        response = self._api_request_handler.send_command(DominoCommand.RETRIEVE_SECRET, key)
        self._api_request_handler.handle_response(response, self._handle_flat_response)

    def retrieve_secrets_by_context(self, context: str) -> None:
        """
        Displays the value of the secrets under the given context.

        :param context: context of the secrets to show the value of
        """
        response = self._api_request_handler.send_command(DominoCommand.RETRIEVE_SECRETS_BY_CONTEXT, context)
        self._api_request_handler.handle_response(response, self._handle_flat_response)

    def lock_secret(self, key: str) -> None:
        """
        Locks (disables retrieval) of the given secret.

        :param key: key of the secret to lock
        """
        response = self._api_request_handler.send_command(DominoCommand.LOCK_SECRET, key)
        self._api_request_handler.handle_response(response)

    def unlock_secret(self, key: str) -> None:
        """
        Unlocks (enables retrieval) of the given secret.

        :param key: key of the secret to unlock
        """
        response = self._api_request_handler.send_command(DominoCommand.UNLOCK_SECRET, key)
        self._api_request_handler.handle_response(response)

    def delete_secret(self, key: str) -> None:
        """
        Deletes the given secret.

        :param key: key of the secret to delete
        """
        response = self._api_request_handler.send_command(DominoCommand.DELETE_SECRET, key)
        self._api_request_handler.handle_response(response)

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
