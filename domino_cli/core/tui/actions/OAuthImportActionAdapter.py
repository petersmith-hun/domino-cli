from textual.app import App

from domino_cli.core.domain.CommandDescriptor import CommandDescriptor
from domino_cli.core.service.CommandProcessor import CommandProcessor
from domino_cli.core.tui.actions import LongRunningActionAdapter


class OAuthImportMessage:
    """
    TODO.
    """
    def __init__(self, deployment_id: str, file_path: str, dry_run: bool):
        self.deployment_id = deployment_id
        self.file_path = file_path
        self.dry_run = dry_run


class OAuthImportActionAdapter(LongRunningActionAdapter[OAuthImportMessage]):
    """
    TODO.
    """
    def __init__(self, app: App, command_processor: CommandProcessor):
        super().__init__(app)
        self._command_processor = command_processor

    def _action(self, event: OAuthImportMessage):
        dry_run_segment = " --dry-run" if event.dry_run else ""

        command = CommandDescriptor(f"oauth-import {event.deployment_id}{dry_run_segment} {event.file_path} ")

        self._command_processor.execute_command(command)
        self._app.call_from_thread(self._show_loading_indicator, False)
