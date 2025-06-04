from getpass import getpass
from typing import List

from domino_cli.core.cli.Logging import error
from domino_cli.core.cli.RuntimeHelper import RuntimeHelper
from domino_cli.core.command.dsl.dsm.DSLMain import SecretCommandProcessor
from domino_cli.core.service.SecretService import SecretService


class CreateSecretCommandProcessor(SecretCommandProcessor):
    """
    SecretCommandProcessor implementation to process the --create <key> <context> secret management command.
    """
    def __init__(self, secret_service: SecretService):
        self._secret_service = secret_service

    def process(self, arguments: List[str]) -> bool:

        RuntimeHelper.unsupported_in_cicd_mode()

        if not len(arguments) == 2:
            error("Invalid arguments, expected usage: secret --create <key> <context> (then you'll be prompted to enter the secret value)")
            return False

        key = arguments.pop(0)
        context = arguments.pop(0)
        value = RuntimeHelper.input_wrapper(lambda: getpass('Enter secret value > '))

        self._secret_service.create_secret(key, context, value)

        return True

    def chain_to(self, arguments: List[str]) -> str | None:
        return None

    def for_subcommand(self) -> str:
        return "--create"
