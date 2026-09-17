import os

from textual import on
from textual.app import App, ComposeResult
from textual.containers import Vertical, HorizontalGroup, VerticalScroll
from textual.widgets import Header, Footer, Label, LoadingIndicator, TabbedContent, TabPane

from domino_cli.core.service.AuthenticationService import AuthenticationService
from domino_cli.core.service.DominoService import DominoService
from domino_cli.core.service.SecretService import SecretService
from domino_cli.core.tui.TUIRuntimeHelper import TUIRuntimeHelper
from domino_cli.core.tui.actions.AuthenticateActionAdapter import AuthenticateActionAdapter
from domino_cli.core.tui.actions.CreateSecretActionAdapter import CreateSecretActionAdapter
from domino_cli.core.tui.actions.DeploymentListActionAdapter import DeploymentListActionAdapter
from domino_cli.core.tui.actions.SecretListActionAdapter import SecretListActionAdapter
from domino_cli.core.tui.actions.SecretManagementActionAdapter import SecretManagementActionAdapter
from domino_cli.core.tui.modals.AuthUtilOptionsModal import AuthUtilOptionsModal
from domino_cli.core.tui.modals.CreateSecretModal import CreateSecretModal
from domino_cli.core.tui.modals.DeploymentDescriptorImportModal import DeploymentDescriptorImportModal
from domino_cli.core.tui.screens.DeploymentListScreen import DeploymentLabel, DeploymentsListScreen
from domino_cli.core.tui.screens.SecretListScreen import SecretListScreen


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
        ("alt+a", "auth_utils", "Auth utils"),
        ("d", "list_deployments", "List deployments"),
        ("alt+d", "import_deployment", "Import deployment"),
        ("s", "list_secrets", "List secrets"),
        ("alt+s", "create_secret", "Create secret"),
        ("q", "quit", "Quit")
    ]

    DEFAULT_CSS = """
    Tabs {
        outline-left: ascii $accent;
        outline-right: ascii $accent;
        padding-left: 2;
        padding-right: 2;
        text-style: italic;
        background: $surface;
    }
    
    VerticalScroll {
        margin-bottom: 1;
        padding-bottom: 1;
    }
    """

    def __init__(self,
                 domino_service: DominoService,
                 secret_service: SecretService,
                 authentication_service: AuthenticationService,
                 version: str):
        super().__init__()
        self._domino_service = domino_service
        self._secret_service = secret_service
        self._version = version
        self._authentication_service = authentication_service
        self._authenticate_action_adapter = AuthenticateActionAdapter(self, authentication_service)
        self._deployment_list_action_adapter = DeploymentListActionAdapter(self, self._domino_service)
        self._secret_list_action_adapter = SecretListActionAdapter(self, self._secret_service)

        self.theme = "textual-dark"
        self.title = f"Domino CLI Next {self._version}"

    def compose(self) -> ComposeResult:
        yield Header()

        with Vertical():
            yield EnvironmentHeader()
            yield LoadingIndicator(id="loading")
            with TabbedContent():
                with TabPane("Deployments", id="tab_deployments"):
                    with VerticalScroll(id="deployments_scroll"):
                        yield DeploymentsListScreen(self._domino_service)
                with TabPane("Secrets", id="tab_secrets"):
                    with VerticalScroll(id="secrets_scroll"):
                        yield SecretListScreen(self._secret_service)

        yield Footer()

    def on_mount(self):
        self.query_one(LoadingIndicator).display = False
        self.query_one(LoadingIndicator).styles.background = self.app.theme_variables["surface"]
        TUIRuntimeHelper.register_toast(self)
        TUIRuntimeHelper.register_is_authenticated_hook(self.query_one("#is_authenticated", Label))

    def action_authenticate(self):
        self._authenticate_action_adapter.execute()

    def action_auth_utils(self):
        self.push_screen(AuthUtilOptionsModal(self._authentication_service))

    def action_list_deployments(self):
        self.query_one(TabbedContent).active = "tab_deployments"
        self._deployment_list_action_adapter.execute()

    def action_import_deployment(self):
        self.query_one(TabbedContent).active = "tab_deployments"
        self.push_screen(DeploymentDescriptorImportModal(self._domino_service))

    def action_list_secrets(self):
        self.query_one(TabbedContent).active = "tab_secrets"
        self._secret_list_action_adapter.execute()

    def action_create_secret(self):
        self.query_one(TabbedContent).active = "tab_secrets"
        self.push_screen(CreateSecretModal(self._secret_service))

    @on(SecretManagementActionAdapter.SecretListRefreshMessage)
    @on(CreateSecretActionAdapter.SecretCreatedMessage)
    def _handle_secret_refresh(self):
        self.action_list_secrets()
