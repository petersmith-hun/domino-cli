from typing import List

from domino_cli.core.cli.Logging import error
from domino_cli.core.cli.RuntimeHelper import RuntimeHelper
from domino_cli.core.command.dsl.dsm.DSLMain import SecretCommandProcessor
from domino_cli.core.service.SecretService import SecretService


class MetadataCommandProcessor(SecretCommandProcessor):
    """
    SecretCommandProcessor implementation to process the --metadata secret management command. Chains forward to --all
    and <key> subcommands.
    """

    def process(self, arguments: List[str]) -> bool:

        RuntimeHelper.unsupported_in_cicd_mode()

        return False

    def chain_to(self, arguments: List[str]) -> str | None:

        if len(arguments) == 0:
            error(f"Too few arguments, first argument must be either: --all | <key>")
            return None

        return "--metadata --all" \
            if arguments[0] == "--all" \
            else "--metadata <key>"

    def for_subcommand(self) -> str:
        return "--metadata"

class MetadataAllCommandProcessor(SecretCommandProcessor):
    """
    SecretCommandProcessor implementation to process the --metadata --all secret management command.
    """
    def __init__(self, secret_service: SecretService):
        self._secret_service = secret_service

    def process(self, arguments: List[str]) -> bool:

        RuntimeHelper.unsupported_in_cicd_mode()
        self._secret_service.get_all_metadata()

        return True

    def chain_to(self, arguments: List[str]) -> str | None:
        return None

    def for_subcommand(self) -> str:
        return "--metadata --all"

class MetadataKeyCommandProcessor(SecretCommandProcessor):
    """
    SecretCommandProcessor implementation to process the --metadata <key> secret management command.
    """
    def __init__(self, secret_service: SecretService):
        self._secret_service = secret_service

    def process(self, arguments: List[str]) -> bool:

        RuntimeHelper.unsupported_in_cicd_mode()

        if not len(arguments) == 1:
            error("Invalid arguments, expected usage: secret --metadata <key>")
            return False

        key = arguments.pop(0)
        self._secret_service.get_metadata_by_key(key)

        return True

    def chain_to(self, arguments: List[str]) -> str | None:
        return None

    def for_subcommand(self) -> str:
        return "--metadata <key>"
