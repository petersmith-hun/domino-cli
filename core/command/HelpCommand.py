from core.domain.CommandDescriptor import CommandDescriptor
from core.command.AbstractCommand import AbstractCommand

_COMMAND_NAME = "help"
_HELP_FILE = "./resource/help.txt"


class HelpCommand(AbstractCommand):
    """
    Prints help contents, containing information about the supported commands.
    """
    def __init__(self):
        super().__init__(_COMMAND_NAME)
        with open(_HELP_FILE, "r") as help_contents:
            self._help_text = help_contents.readlines()

    def execute_command(self, command_descriptor: CommandDescriptor) -> None:
        [print(line, end="") for line in self._help_text]
