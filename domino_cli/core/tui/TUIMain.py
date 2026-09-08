import os

from textual.app import App, ComposeResult
from textual.containers import Vertical, HorizontalGroup, VerticalScroll
from textual.widgets import Header, Footer, Label, LoadingIndicator

from domino_cli.core.service.CommandProcessor import CommandProcessor
from domino_cli.core.service.DominoService import DominoService
from domino_cli.core.tui.TUIRuntimeHelper import TUIRuntimeHelper
from domino_cli.core.tui.actions.AuthenticateActionAdapter import AuthenticateActionAdapter
from domino_cli.core.tui.screens.DeploymentListScreen import DeploymentLabel, DeploymentsListScreen


class EnvironmentHeader(HorizontalGroup):
    DEFAULT_CSS = """
    EnvironmentHeader {
        padding: 1 2;
        background: $surface;
        outline: ascii $accent;
        text-style: bold;
    }
    """
    def __init__(self):
        super().__init__(
            DeploymentLabel(f"Connected to Domino Coordinator on {os.getenv("DOMINO_BASE_URL")}", long_field=True),
            Label("Authenticated: "),
            Label("❌", id="is_authenticated")
        )


class TUIMain(App):

    BINDINGS = [
        ("a", "authenticate", "Authenticate"),
        ("d", "list_deployments", "List deployments"),
        ("q", "quit", "Quit")
    ]

    def __init__(self, command_processor: CommandProcessor, domino_service: DominoService, version: str):
        super().__init__()
        self._command_processor = command_processor
        self._domino_service = domino_service
        self._version = version
        self._authenticate_action_adapter = AuthenticateActionAdapter(self, self._command_processor)

        self.theme = "textual-dark"
        self.title = f"Domino CLI Next {self._version}"

    def compose(self) -> ComposeResult:
        yield Header()

        with Vertical():
            yield EnvironmentHeader()
            yield LoadingIndicator(id="loading")
            with VerticalScroll(id="deployments_scroll"):
                yield DeploymentsListScreen(self._domino_service, self._command_processor)

        yield Footer()

    def on_mount(self):
        self.query_one(LoadingIndicator).display = False
        self.query_one(LoadingIndicator).styles.background = self.app.theme_variables["surface"]
        TUIRuntimeHelper.register_toast(self)
        TUIRuntimeHelper.register_is_authenticated_hook(self.query_one("#is_authenticated", Label))

    def action_authenticate(self):
        self._authenticate_action_adapter.execute()

    def action_list_deployments(self):
        self.query_one(DeploymentsListScreen).execute()
