from domino_cli.core.domain.CommandDescriptor import CommandDescriptor
from domino_cli.core.service.CommandProcessor import CommandProcessor

_PROMPT = "\nDomino CLI > "


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
