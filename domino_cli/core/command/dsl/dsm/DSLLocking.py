from typing import List

from domino_cli.core.cli.Logging import error
from domino_cli.core.cli.RuntimeHelper import RuntimeHelper
from domino_cli.core.command.dsl.dsm.DSLMain import SecretCommandProcessor
from domino_cli.core.service.SecretService import SecretService


class LockSecretCommandProcessor(SecretCommandProcessor):
    """
    SecretCommandProcessor implementation to process the --lock <key> secret management command.
    """
    def __init__(self, secret_service: SecretService):
        self._secret_service = secret_service

    def process(self, arguments: List[str]) -> bool:

        RuntimeHelper.unsupported_in_cicd_mode()

        if not len(arguments) == 1:
            error("Invalid arguments, expected usage: secret --lock <key>")
            return False

        key = arguments.pop(0)
        self._secret_service.lock_secret(key)

        return True

    def chain_to(self, arguments: List[str]) -> str | None:
        return None

    def for_subcommand(self) -> str:
        return "--lock"

class UnlockSecretCommandProcessor(SecretCommandProcessor):
    """
    SecretCommandProcessor implementation to process the --unlock <key> secret management command.
    """
    def __init__(self, secret_service: SecretService):
        self._secret_service = secret_service

    def process(self, arguments: List[str]) -> bool:

        RuntimeHelper.unsupported_in_cicd_mode()

        if not len(arguments) == 1:
            error("Invalid arguments, expected usage: secret --unlock <key>")
            return False

        key = arguments.pop(0)
        self._secret_service.unlock_secret(key)

        return True

    def chain_to(self, arguments: List[str]) -> str | None:
        return None

    def for_subcommand(self) -> str:
        return "--unlock"
