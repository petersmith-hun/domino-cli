from typing import List

from textual.widgets import Label

from domino_cli.core.service.DominoService import DominoService
from domino_cli.core.tui.modals import OptionsModalScreen, CustomModalListItem
from domino_cli.core.tui.modals.LifecycleOperationModal import LifecycleOperationModal
from domino_cli.core.tui.modals.OAuthDescriptorImportModal import OAuthDescriptorImportModal


class DeploymentOptionsModal(OptionsModalScreen):

    def __init__(self, domino_service: DominoService, deployment_id: str):
        super().__init__()
        self._deployment_id = deployment_id
        self._domino_service = domino_service

    def _get_title(self) -> Label:
        return Label(f"{self._deployment_id} lifecycle operations")

    def _get_items(self) -> List[CustomModalListItem]:

        return [
            CustomModalListItem("deploy_latest", "Deploy latest",
                                "Deploys the latest, automatically resolved version of the application"),
            CustomModalListItem("deploy_version", "Deploy specific version",
                                "Deploy a specific version of the application"),
            CustomModalListItem("start", "Start application",
                                "Starts the currently deployed version of the application"),
            CustomModalListItem("restart", "Restart application",
                                "Restart the currently running application"),
            CustomModalListItem("stop", "Stop application",
                                "Stops the currently running application"),
            CustomModalListItem("info", "Show application info",
                                "Shows information about the running application"),
            CustomModalListItem("import_oauth", "Import OAuth configuration",
                                "Imports OAuth configuration for the application"),
        ]

    def _on_option_selected(self, item_id: str) -> None:

        if item_id in ["deploy_latest", "deploy_version", "start", "restart", "stop", "info"]:
            self.app.push_screen(LifecycleOperationModal(self._domino_service, self._deployment_id, operation=item_id))

        if item_id == "import_oauth":
            self.app.push_screen(OAuthDescriptorImportModal(self._domino_service, self._deployment_id))
