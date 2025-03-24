from domino_cli.core.cli.Logging import info
from domino_cli.core.command.AbstractCommand import AbstractCommand
from domino_cli.core.domain.CommandDescriptor import CommandDescriptor

_COMMAND_NAME = "exit"


class ExitCommand(AbstractCommand):
    """
    Exit command implementation.
    Interrupts CLI execution loop.
    """
    def __init__(self):
        super().__init__(_COMMAND_NAME)

    def execute_command(self, command_descriptor: CommandDescriptor) -> None:
        info("Bye!")
