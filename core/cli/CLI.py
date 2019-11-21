from core.domain.CommandDescriptor import CommandDescriptor
from core.service.CommandProcessor import CommandProcessor

_PROMPT = "Domino CLI > "


class CLI:
    """
    Command line interface (CLI) executor.
    """
    def __init__(self, command_processor: CommandProcessor):
        self._command_processor = command_processor

    def run_loop(self) -> None:
        """
        Runs CLI command execution loop until an exit command terminates it.
        """
        while True:
            command = CommandDescriptor(input(_PROMPT))
            continue_loop = self._command_processor.execute_command(command)

            if not continue_loop:
                break