from abc import abstractmethod
from abc import ABCMeta

from core.domain.CommandDescriptor import CommandDescriptor


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
