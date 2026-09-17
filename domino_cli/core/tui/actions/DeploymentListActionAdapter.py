from textual.app import App
from textual.widgets import ListView

from domino_cli.core.domain.CustomExceptions import DominoServiceException
from domino_cli.core.service.DominoService import DominoService
from domino_cli.core.tui.actions import LongRunningActionAdapter
from domino_cli.core.tui.screens.DeploymentListScreen import DeploymentListHeader, DeploymentListItem


class DeploymentListActionAdapter(LongRunningActionAdapter[None]):
    """
    TODO.
    """
    def __init__(self, app: App, domino_service: DominoService):
        super().__init__(app)
        self._domino_service = domino_service

    def _action(self, event: None):

        try:
            deployments = self._domino_service.get_deployments_page()

        except DominoServiceException as exc:
            self._app.call_from_thread(lambda: self._app.notify(f"Error fetching deployments: {str(exc)}", title="Failed fetching deployments", severity="error"))
            return

        if deployments is None or len(deployments) == 0:
            return

        deployments_list_view = self._app.query_one("#deployments", ListView)

        if deployments_list_view.children:
            self._app.call_from_thread(lambda: deployments_list_view.clear())

        self._app.call_from_thread(lambda: deployments_list_view.append(DeploymentListHeader()))

        for index, deployment in enumerate(deployments):
            item = DeploymentListItem(deployment)

            if index == 0:
                item.styles.border_top = ("ascii", self._app.theme_variables["accent"])

            self._app.call_from_thread(lambda: deployments_list_view.append(item))
