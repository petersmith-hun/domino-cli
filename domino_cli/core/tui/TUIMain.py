import os

from textual import on
from textual.app import App, ComposeResult
from textual.containers import Vertical, HorizontalGroup, VerticalScroll
from textual.widgets import Header, Footer, Label, LoadingIndicator, TabbedContent, TabPane

from domino_cli.core.tui.TUIRuntimeHelper import TUIRuntimeHelper
from domino_cli.core.tui.actions.CreateSecretActionAdapter import CreateSecretActionAdapter
from domino_cli.core.tui.actions.SecretManagementActionAdapter import SecretManagementActionAdapter
from domino_cli.core.tui.factory.TUIMainComponentsFactory import TUIMainComponentsFactory
from domino_cli.core.tui.factory.TUIWizardComponentsFactory import TUIWizardComponentsFactory
from domino_cli.core.tui.screens.DeploymentListScreen import DeploymentLabel, DeploymentsListScreen
from domino_cli.core.tui.screens.SecretListScreen import SecretListScreen
from domino_cli.core.tui.screens.WizardSelectorScreen import WizardSelectorScreen


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
        ("w", "wizards", "Wizards"),
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

    def __init__(self, version: str, tui_main_components_factory: TUIMainComponentsFactory,
                 tui_wizard_components_factory: TUIWizardComponentsFactory):
        super().__init__()
        self._version = version
        self._tui_main_components_factory = tui_main_components_factory
        self._tui_wizard_components_factory = tui_wizard_components_factory
        self._authenticate_action_adapter = self._tui_main_components_factory.create_authenticate_action_adapter(self)
        self._deployment_list_action_adapter = self._tui_main_components_factory.create_deployment_list_action_adapter(self)
        self._secret_list_action_adapter = self._tui_main_components_factory.create_create_secret_action_adapter(self)

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
                        yield self._tui_main_components_factory.create_deployment_list_screen()
                with TabPane("Secrets", id="tab_secrets"):
                    with VerticalScroll(id="secrets_scroll"):
                        yield self._tui_main_components_factory.create_secret_list_screen()
                with TabPane("Wizards", id="tab_wizards"):
                    with VerticalScroll(id="wizards_scroll"):
                        yield self._tui_wizard_components_factory.create_wizard_selector_screen()

        yield Footer()

    def on_mount(self):
        self.query_one(LoadingIndicator).display = False
        self.query_one(LoadingIndicator).styles.background = self.app.theme_variables["surface"]
        TUIRuntimeHelper.register_toast(self)
        TUIRuntimeHelper.register_is_authenticated_hook(self.query_one("#is_authenticated", Label))

    def action_authenticate(self):
        self._authenticate_action_adapter.execute()

    def action_auth_utils(self):
        self.push_screen(self._tui_main_components_factory.create_auth_util_options_modal())

    def action_list_deployments(self):
        self.query_one(TabbedContent).active = "tab_deployments"
        self._deployment_list_action_adapter.execute()

    def action_import_deployment(self):
        self.query_one(TabbedContent).active = "tab_deployments"
        self.push_screen(self._tui_main_components_factory.create_deployment_descriptor_import_modal())
        self.query_one(DeploymentsListScreen).focus()

    def action_list_secrets(self):
        self.query_one(TabbedContent).active = "tab_secrets"
        self._secret_list_action_adapter.execute()
        self.query_one(SecretListScreen).focus()

    def action_create_secret(self):
        self.query_one(TabbedContent).active = "tab_secrets"
        self.push_screen(self._tui_main_components_factory.create_create_secret_modal())

    def action_wizards(self):
        self.query_one(TabbedContent).active = "tab_wizards"
        self.query_one(WizardSelectorScreen).focus()

    @on(SecretManagementActionAdapter.SecretListRefreshMessage)
    @on(CreateSecretActionAdapter.SecretCreatedMessage)
    def _handle_secret_refresh(self):
        self.action_list_secrets()
