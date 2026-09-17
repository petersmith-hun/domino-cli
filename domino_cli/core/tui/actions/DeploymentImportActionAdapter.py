from textual.app import App

from domino_cli.core.domain.CustomExceptions import DominoServiceException
from domino_cli.core.service.DominoService import DominoService
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
    def __init__(self, app: App, domino_service: DominoService):
        super().__init__(app)
        self._domino_service = domino_service

    def _action(self, event: DeploymentImportMessage):

        try:
            self._domino_service.import_definition(event.file_path)
            self._app.notify(f"Successfully imported deployment definition from [i]{event.file_path}[/i]",
                             title="Deployment definition import completed", severity="information", markup=True, timeout=10)

        except DominoServiceException as exc:
            self._app.notify(str(exc), title="Failed to import deployment definition", severity="error")
