from textual.app import App

from domino_cli.core.domain.CommandDescriptor import CommandDescriptor
from domino_cli.core.service.CommandProcessor import CommandProcessor
from domino_cli.core.tui.actions import LongRunningActionAdapter


class AuthenticateActionAdapter(LongRunningActionAdapter[None]):
    """
    TODO.
    """
    def __init__(self, app: App, command_processor: CommandProcessor):
        super().__init__(app)
        self._command_processor = command_processor

    def _action(self, event: None):
        command = CommandDescriptor("auth --open-session")
        self._command_processor.execute_command(command)
