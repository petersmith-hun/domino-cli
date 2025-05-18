from typing import List

from domino_cli.core.cli.Logging import error
from domino_cli.core.cli.RuntimeHelper import RuntimeHelper
from domino_cli.core.command.dsl.dsm.DSLMain import SecretCommandProcessor
from domino_cli.core.service.SecretService import SecretService


class DeleteSecretCommandProcessor(SecretCommandProcessor):
    """
    SecretCommandProcessor implementation to process the --delete <key> secret management command.
    """
    def __init__(self, secret_service: SecretService):
        self._secret_service = secret_service

    def process(self, arguments: List[str]) -> bool:

        RuntimeHelper.unsupported_in_cicd_mode()

        if not len(arguments) == 1:
            error("Invalid arguments, expected usage: secret --delete <key>")
            return False

        key = arguments.pop(0)
        self._secret_service.delete_secret(key)

        return True

    def chain_to(self, arguments: List[str]) -> str | None:
        return None

    def for_subcommand(self) -> str:
        return "--delete"
