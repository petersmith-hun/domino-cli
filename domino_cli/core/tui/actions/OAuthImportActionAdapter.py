from textual.app import App

from domino_cli.core.domain.CustomExceptions import DominoServiceException
from domino_cli.core.service.DominoService import DominoService
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
    def __init__(self, app: App, domino_service: DominoService):
        super().__init__(app)
        self._domino_service = domino_service

    def _action(self, event: OAuthImportMessage):

        try:
            self._domino_service.import_oauth_descriptor(event.deployment_id, event.dry_run, event.file_path)
            self._app.notify(f"Successfully imported OAuth definition from [i]{event.file_path}[/i]",
                             title="OAuth definition import completed", severity="information", markup=True, timeout=10)

        except DominoServiceException as exc:
            self._app.notify(str(exc), title="Failed to import OAuth definition", severity="error")
