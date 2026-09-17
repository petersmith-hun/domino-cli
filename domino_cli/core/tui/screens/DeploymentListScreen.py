from typing import cast

from textual.containers import HorizontalGroup
from textual.widgets import Label, ListItem, ListView

from domino_cli.core.domain.Deployments import DeploymentSummary
from domino_cli.core.service.DominoService import DominoService
from domino_cli.core.tui.modals.DeploymentOptionsModal import DeploymentOptionsModal


class DeploymentLabel(Label):
    """
    TODO.
    """

    DEFAULT_CSS = """
    DeploymentLabel {
        padding: 0 2;
    }
    """
    def __init__(self, text: str, long_field: bool = False):
        super().__init__(text)
        if long_field:
            self.styles.width = "2fr"
        else:
            self.styles.width = "1fr"


class DeploymentListItem(ListItem):
    """
    TODO.
    """

    DEFAULT_CSS = """
    DeploymentListItem {
        padding: 1 2;
        outline-top: none;
        outline-bottom: none;
        outline-left: ascii $accent;
        outline-right: ascii $accent;
    }
    """

    def __init__(self, deployment: DeploymentSummary):

        labels = [
            DeploymentLabel(deployment.id),
            DeploymentLabel(deployment.source_type),
            DeploymentLabel(deployment.execution_type),
            DeploymentLabel(deployment.home, True),
            DeploymentLabel(deployment.resource, True)
        ]

        if deployment.locked == "Locked":
            labels.append(DeploymentLabel("Locked"))
        else:
            labels.append(DeploymentLabel("Yes" if deployment.locked else "No"))

        super().__init__(HorizontalGroup(*labels))
        self.deployment_id = deployment.id


class DeploymentListHeader(DeploymentListItem):
    """
    TODO.
    """

    DEFAULT_CSS = """
    DeploymentListHeader {
        text-style: bold;
        background: $boost;
    }
    """
    _HEADER = DeploymentSummary({
        "id": "ID",
        "sourceType": "Source Type",
        "executionType": "Execution Type",
        "home": "Home",
        "resource": "Resource",
        "locked": "Locked"
    })

    def __init__(self):
        super().__init__(self._HEADER)


class DeploymentsListScreen(ListView):
    """
    TODO.
    """

    DEFAULT_CSS = """
    DeploymentsListScreen {
        background: $surface;
        outline-left: ascii $accent;
        outline-right: ascii $accent;
        outline-bottom: ascii $accent;
    }
    """
    def __init__(self, domino_service: DominoService):
        super().__init__(id="deployments")
        self._domino_service = domino_service

    def action_select_cursor(self) -> None:

        if isinstance(self.highlighted_child, DeploymentListHeader):
            return

        deployment = cast(DeploymentListItem, self.highlighted_child)
        self.app.push_screen(DeploymentOptionsModal(self._domino_service, deployment.deployment_id))
