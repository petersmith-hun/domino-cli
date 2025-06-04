from abc import ABCMeta, abstractmethod
from typing import List

from domino_cli.core.cli.Logging import error


class SecretCommandProcessor(object, metaclass=ABCMeta):
    """
    DSL processor interface for secret management commands.
    """
    @abstractmethod
    def process(self, arguments: List[str]) -> bool:
        """
        Final state of the command, executes the recognized management operation.

        :param arguments: current command argument list
        :return: boolean flag indicating if the command was processed
        """
        pass

    @abstractmethod
    def chain_to(self, arguments: List[str]) -> str | None:
        """
        Defines the further chaining logic. Returns none if further chaining is not possible either because of an error,
        or if the chain reached a final state. May drop the first argument of the list.

        :param arguments: current command argument list
        :return: next processor name or None if further chaining is not possible
        """
        pass

    @abstractmethod
    def for_subcommand(self) -> str:
        """
        Indicates the processor name to be used in chaining.

        :return: processor name
        """
        pass

class MainSecretCommandProcessor(SecretCommandProcessor):
    """
    Main command processor, i.e. the entry point of secret management command processing. Entry argument token is
    "secret", and may move on to any of the known commands (--create, --metadata, --retrieve, --lock, --unlock, --delete).
    """

    valid_subcommands = ["--create", "--metadata", "--retrieve", "--lock", "--unlock", "--delete"]

    def process(self, arguments: List[str]) -> bool:
        return False

    def chain_to(self, arguments: List[str]) -> str | None:

        if len(arguments) == 0:
            error(f"Too few arguments, first argument must be either: {" | ".join(self.valid_subcommands)}")
            return None

        subcommand = arguments.pop(0)

        if subcommand not in self.valid_subcommands:
            error(f"Invalid subcommand, first argument must be either: {" | ".join(self.valid_subcommands)}")
            return None

        else:
            return subcommand

    def for_subcommand(self) -> str:
        return "secret"
