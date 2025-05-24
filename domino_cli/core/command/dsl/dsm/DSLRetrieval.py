from typing import List

from domino_cli.core.cli.Logging import error
from domino_cli.core.command.dsl.dsm.DSLMain import SecretCommandProcessor
from domino_cli.core.service.SecretService import SecretService


class RetrievalSecretCommandProcessor(SecretCommandProcessor):
    """
    SecretCommandProcessor implementation to process the --retrieve secret management command. Chains forward to --key
    or --context subcommands.
    """

    valid_subcommands = ["--key", "--context"]

    def process(self, arguments: List[str]) -> bool:
        return False

    def chain_to(self, arguments: List[str]) -> str | None:

        if len(arguments) < 1:
            error(f"Too few arguments, must be either: --key <key> | --context <context>")
            return None

        if len(arguments) > 2:
            error(f"Too many arguments, must be either: --key <key> | --context <context>")
            return None

        subcommand = arguments.pop(0)

        if subcommand not in self.valid_subcommands:
            error(f"Invalid subcommand, first argument must be either: {" | ".join(self.valid_subcommands)}")
            return None

        return f"--retrieve {subcommand}"

    def for_subcommand(self) -> str:
        return "--retrieve"

class RetrieveByKeySecretCommandProcessor(SecretCommandProcessor):
    """
    SecretCommandProcessor implementation to process the --retrieve --key <key> secret management command.
    """
    def __init__(self, secret_service: SecretService):
        self._secret_service = secret_service

    def process(self, arguments: List[str]) -> bool:

        if not len(arguments) == 1:
            error("Invalid arguments, expected usage: secret --retrieve --key <key>")
            return False

        key = arguments.pop(0)
        self._secret_service.retrieve_secret_by_key(key)

        return True

    def chain_to(self, arguments: List[str]) -> str | None:
        return None

    def for_subcommand(self) -> str:
        return "--retrieve --key"

class RetrieveByContextSecretCommandProcessor(SecretCommandProcessor):
    """
    SecretCommandProcessor implementation to process the --retrieve --context <context> secret management command.
    """
    def __init__(self, secret_service: SecretService):
        self._secret_service = secret_service

    def process(self, arguments: List[str]) -> bool:

        if not len(arguments) == 1:
            error("Invalid arguments, expected usage: secret --retrieve --context <context>")
            return False

        context = arguments.pop(0)
        self._secret_service.retrieve_secrets_by_context(context)

        return True

    def chain_to(self, arguments: List[str]) -> str | None:
        return None

    def for_subcommand(self) -> str:
        return "--retrieve --context"
