from core.domain.CommandDescriptor import CommandDescriptor
from core.command.AbstractCommand import AbstractCommand

_COMMAND_NAME = "exit"


class ExitCommand(AbstractCommand):
    """
    Exit command implementation.
    Interrupts CLI execution loop.
    """
    def __init__(self):
        super().__init__(_COMMAND_NAME)

    def execute_command(self, command_descriptor: CommandDescriptor) -> None:
        print("Bye!")
