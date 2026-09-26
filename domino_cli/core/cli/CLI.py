from domino_cli.core.cli.Logging import TerminalColor, get_color
from domino_cli.core.cli.RuntimeHelper import RuntimeHelper
from domino_cli.core.domain.CommandDescriptor import CommandDescriptor
from domino_cli.core.service.CommandProcessor import CommandProcessor

_PROMPT = f"\n{get_color(TerminalColor.BLUE)}Domino CLI > {get_color(TerminalColor.NORMAL)}"


class CLI:
    """
    Command line interface (CLI) executor.
    """
    def __init__(self, command_processor: CommandProcessor):
        self._command_processor = command_processor

    def run_loop(self) -> None:
        """
        Executes a single command (passed from the command line) in CI/CD mode, otherwise runs CLI command execution
        loop until an exit command terminates it.
        """
        if RuntimeHelper.is_cicd_mode():
            command = CommandDescriptor(RuntimeHelper.get_cicd_command_line())
            self._command_processor.execute_command(command)
            return

        while True:
            command = CommandDescriptor(RuntimeHelper.input_wrapper(lambda: input(_PROMPT)))
            continue_loop = self._command_processor.execute_command(command)

            if not continue_loop:
                break
