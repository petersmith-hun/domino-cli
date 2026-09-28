from abc import ABCMeta
from abc import abstractmethod

from domino_cli.core.cli.Logging import info
from domino_cli.core.domain.CommandDescriptor import CommandDescriptor
from domino_cli.core.domain.DominoCommand import DominoCommand


class AbstractCommand(object, metaclass=ABCMeta):
    """
    Command interface.
    Implementations should contain the associated logic for each supported command.
    """
    def __init__(self, command_name: str):
        self._command_name = command_name

    def is_applicable(self, command_descriptor: CommandDescriptor) -> bool:
        """
        Checks if the currently selected command implementation supports the requested command.

        :param command_descriptor: CommandDescriptor object containing the requested command with its arguments
        :return: boolean, true if the implementation is applicable, false otherwise
        """
        return command_descriptor.command == self._command_name

    @abstractmethod
    def execute_command(self, command_descriptor: CommandDescriptor) -> None:
        """
        Executes implemented command logic.

        :param command_descriptor: CommandDescriptor object containing the requested command with its arguments
        """
        pass

    def _print_result(self, command: DominoCommand, application: str, result: object | dict[str, str]) -> None:

        info("Command {0} successfully executed on application {1}".format(command.name, application))
        info(" --- Response details ---")
        result_dict = result if isinstance(result, dict) else result.__dict__
        for key, value in result_dict.items():
            info("{:>20}: {}".format(key, value))
        print()
