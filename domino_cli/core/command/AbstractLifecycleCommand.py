from domino_cli.core.cli.Logging import warning
from domino_cli.core.command.AbstractCommand import AbstractCommand
from domino_cli.core.domain.CommandDescriptor import CommandDescriptor
from domino_cli.core.domain.DominoCommand import DominoCommand
from domino_cli.core.service.DominoService import DominoService


class AbstractLifecycleCommand(AbstractCommand):
    """
    Abstract base class for simple lifecycle commands (with only the name of the application as parameter).
    """
    def __init__(self, command_name: str, domino_service: DominoService, domino_command: DominoCommand):
        super().__init__(command_name)
        self._domino_service = domino_service
        self._domino_command = domino_command

    def execute_command(self, command_descriptor: CommandDescriptor) -> None:
        """
        Executes a simple lifecycle command (currently supported commands are start, stop, restart).
        Argument array must contain the name of the application. Besides, --roll and --instance flags can be used to
        trigger rolling all instances of a multi-instance deployment or just a specific instance, respectively.

        :param command_descriptor: CommandDescriptor object containing the command arguments
        """
        if len(command_descriptor.arguments) == 0:
            warning("Application name required")
        else:

            roll = "--roll" in command_descriptor.arguments
            instance = command_descriptor.arguments[2] \
                if "--instance" in command_descriptor.arguments and len(command_descriptor.arguments) == 3 \
                else None

            self._domino_service.execute_lifecycle_command(self._domino_command, command_descriptor.arguments[0],
                                                           version=None, roll=roll, instance=instance)
