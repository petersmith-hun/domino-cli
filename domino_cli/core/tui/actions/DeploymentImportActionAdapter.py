from textual.app import App

from domino_cli.core.domain.CommandDescriptor import CommandDescriptor
from domino_cli.core.service.CommandProcessor import CommandProcessor
from domino_cli.core.tui.actions import LongRunningActionAdapter


class DeploymentImportMessage:
    """
    TODO.
    """
    def __init__(self, file_path: str):
        self.file_path = file_path


class DeploymentImportActionAdapter(LongRunningActionAdapter[DeploymentImportMessage]):
    """
    TODO.
    """
    def __init__(self, app: App, command_processor: CommandProcessor):
        super().__init__(app)
        self._command_processor = command_processor

    def _action(self, event: DeploymentImportMessage):
        command = CommandDescriptor(f"import {event.file_path}")

        self._command_processor.execute_command(command)
        self._app.call_from_thread(self._show_loading_indicator, False)
