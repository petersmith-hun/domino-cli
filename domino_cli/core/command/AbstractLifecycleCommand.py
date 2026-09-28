from domino_cli.core.cli.Logging import warning, error
from domino_cli.core.cli.RuntimeHelper import RuntimeHelper
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
            return

        application = command_descriptor.arguments[0]

        roll = "--roll" in command_descriptor.arguments
        instance = command_descriptor.arguments[2] \
            if "--instance" in command_descriptor.arguments and len(command_descriptor.arguments) == 3 \
            else None

        try:
            result = self._domino_service.execute_lifecycle_command(self._domino_command, application, roll=roll, instance=instance)
            self._print_result(self._domino_command, application, result)

        except Exception as exc:
            error("Failed to execute command {0} on application {1} - Domino call result is: {2}"
                  .format(self._domino_command.name, application, str(exc)))
            RuntimeHelper.exit_with_error_in_cicd_mode()
