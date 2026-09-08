import os
import typing

from textual import on
from textual.app import App, ComposeResult
from textual.containers import Vertical, HorizontalGroup, VerticalScroll, VerticalGroup
from textual.message import Message
from textual.screen import ModalScreen
from textual.widget import Widget
from textual.widgets import Header, Footer, Label, LoadingIndicator, ListView, ListItem, OptionList, Rule, Checkbox, \
    Input, Button
from textual.widgets.option_list import Option
from typing_extensions import Literal

from domino_cli.core.domain.CommandDescriptor import CommandDescriptor
from domino_cli.core.service.CommandProcessor import CommandProcessor
from domino_cli.core.service.SecretService import SecretService
from domino_cli.core.tui.TUIRuntimeHelper import TUIRuntimeHelper


class DeploymentLabel(Label):

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

    DEFAULT_CSS = """
    DeploymentListItem {
        padding: 1 2;
        outline-top: none;
        outline-bottom: none;
        outline-left: ascii $accent;
        outline-right: ascii $accent;
    }
    """

    def __init__(self, deployment: dict[str, str]):
        super().__init__(
            HorizontalGroup(
                DeploymentLabel(deployment["id"]),
                DeploymentLabel(deployment["sourceType"]),
                DeploymentLabel(deployment["executionType"]),
                DeploymentLabel(deployment["home"], True),
                DeploymentLabel(deployment["resource"], True),
                DeploymentLabel("Yes" if deployment["locked"] else "No")
            )
        )
        self.deployment_id = deployment["id"]


class DeploymentListHeader(DeploymentListItem):
    DEFAULT_CSS = """
    DeploymentListHeader {
        text-style: bold;
        background: $boost;
    }
    """
    def __init__(self):
        super().__init__({
            "id": "ID",
            "sourceType": "Source Type",
            "executionType": "Execution Type",
            "home": "Home",
            "resource": "Resource",
            "locked": True
        })


class DeploymentsListView(ListView):
    DEFAULT_CSS = """
    DeploymentsListView {
        background: $surface;
        outline-left: ascii $accent;
        outline-right: ascii $accent;
        outline-bottom: ascii $accent;
    }
    """
    def __init__(self):
        super().__init__(id="deployments")

    def action_select_cursor(self) -> None:
        deployment = typing.cast(DeploymentListItem, self.highlighted_child)
        if deployment and deployment.deployment_id != "ID":
            self.app.push_screen(DeploymentOptionsModal(deployment.deployment_id))


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


class DeploymentOptionList(OptionList):

    def __init__(self, deployment_id: str):
        super().__init__(
            Option("Deploy latest", id="deploy_latest"),
            Option("Deploy specific version", id="deploy_version"),
            Option("Start application", id="start"),
            Option("Restart application", id="restart"),
            Option("Stop application", id="stop"),
            Option("Show application info", id="info"),
            Option("Import OAuth configuration", id="import_oauth"),
        )
        self._deployment_id = deployment_id


    def action_select(self) -> None:

        if self.highlighted_option is None:
            return

        option_id = self.highlighted_option.id

        if option_id in ["deploy_latest", "deploy_version", "start", "restart", "stop", "info"]:
            self.app.push_screen(LifecycleOperationModal(self._deployment_id, operation=option_id))


class CustomModalScreen(ModalScreen):

    BINDINGS = [
        ("c", "app.pop_screen", "Close")
    ]

    DEFAULT_CSS = """
        CustomModalScreen {
            align: center middle;
        }
        
        #custom_modal_frame {
            background: $boost;
            outline: ascii $accent;
            max-width: 80%;
            max-height: 80%;
            align: center middle;
        }
        
        #custom_modal_controls {
            padding: 0 3;
            outline-left: ascii $accent;
            outline-right: ascii $accent;
            # outline-bottom: ascii $accent;
        }
        """

    def __init__(self, deployment_id: str):
        super().__init__()
        self._deployment_id = deployment_id

    def compose(self) -> ComposeResult:
        with Vertical(id="custom_modal_frame"):
            with VerticalGroup(id="custom_modal_controls"):
                yield self._get_title()
                yield Rule()
                for widget in self._get_content():
                    yield widget
            yield Footer(id="custom_modal_footer")

    def _get_title(self) -> Label:
        pass

    def _get_content(self) -> typing.List[Widget]:
        pass

class DeploymentOptionsModal(CustomModalScreen):

    def __init__(self, deployment_id: str):
        super().__init__(deployment_id)

    def _get_title(self) -> Label:
        return Label(f"{self._deployment_id} lifecycle operations")

    def _get_content(self) -> typing.List[Widget]:
        return [
            DeploymentOptionList(self._deployment_id)
        ]


class LifecycleOperationModal(CustomModalScreen):

    class Submitted(Message):
        def __init__(self, operation: str, deployment_id: str, roll: bool, instance: str, version: str | None):
            self.operation = operation
            self.deployment_id = deployment_id
            self.roll = roll
            self.instance = instance
            self.version = version
            super().__init__()

    DEFAULT_CSS = """
        #custom_modal_frame {
            max-width: 50;
            max-height: 30;
        }
    
        .mt2 {
            margin-top: 2;
        }
        
        .full_width {
            width: 100%;
        }
        
        .align_right {
            align-horizontal: right;
        }
        """

    _SYMBOL_MAP = {
        "deploy_latest": "☁",
        "deploy_version": "☁",
        "start": "▶",
        "stop": "⏹",
        "restart": "⟳",
        "info": "ℹ"
    }

    def __init__(self, deployment_id: str, operation: Literal["deploy_latest", "deploy_version", "start", "stop", "restart", "info"]):
        super().__init__(deployment_id)
        self._operation = operation

    def _get_title(self) -> Label:
        return Label(f"{self._SYMBOL_MAP.get(self._operation)} {self._operation} {self._deployment_id}")

    def _get_content(self) -> typing.List[Widget]:

        show_version_input = self._operation == "deploy_version" or self._operation == "deploy_latest"
        version = "latest" if self._operation == "deploy_latest" else ""

        widgets: list[Widget] = []

        if show_version_input:
            widgets.append(Input(
                placeholder="Version",
                id="version",
                classes="full_width",
                value=version,
                disabled=self._operation == "deploy_latest"
            ))

        if self._operation != "info":
            widgets.append(Checkbox("Roll all instances", id="roll", classes="full_width"))

        widgets.extend([
            Input(
                placeholder="Instance suffix",
                id="instance_suffix",
                max_length=16,
                classes="mt2 full_width",
            ),
            HorizontalGroup(
                Button("OK", id="execute_lifecycle_command", variant="primary", classes="mt2"),
                classes="align_right full_width",
            ),
        ])

        return [VerticalGroup(*widgets)]

    @on(Button.Pressed)
    def _handle_lifecycle_operation(self):

        roll_checkbox = self.query_one_optional("#roll", Checkbox)
        version_input = self.query_one_optional("#version", Input)

        lifecycle_request_message = LifecycleOperationModal.Submitted(
            operation="deploy" if self._operation.startswith("deploy") else self._operation,
            deployment_id=self._deployment_id,
            roll=roll_checkbox.value if isinstance(roll_checkbox, Checkbox) else False,
            instance=self.query_one("#instance_suffix", Input).value,
            version=version_input.value if isinstance(version_input, Input) else None,
        )

        self.app.post_message(lifecycle_request_message)


class TUIMain(App):

    BINDINGS = [
        ("a", "authenticate", "Authenticate"),
        ("d", "list_deployments", "List deployments"),
        ("q", "quit", "Quit")
    ]

    def __init__(self, command_processor: CommandProcessor, secret_service: SecretService, version: str):
        super().__init__()
        self._command_processor = command_processor
        self._secret_service = secret_service
        self._version = version

        self.theme = "textual-dark"
        self.title = f"Domino CLI Next {self._version}"

    def compose(self) -> ComposeResult:
        yield Header()

        with Vertical():
            yield EnvironmentHeader()
            yield LoadingIndicator(id="loading")
            with VerticalScroll(id="deployments_scroll"):
                yield DeploymentsListView()

        yield Footer()

    def on_mount(self):
        self._show_loading_indicator(False)
        self.query_one(LoadingIndicator).styles.background = self.app.theme_variables["surface"]
        TUIRuntimeHelper.register_toast(self)
        TUIRuntimeHelper.register_is_authenticated_hook(self.query_one("#is_authenticated", Label))

    def action_authenticate(self):
        self._show_loading_indicator(True)
        self.run_worker(self._authenticate, thread=True)

    def action_list_deployments(self):
        self._show_loading_indicator(True)
        self.run_worker(self._list_deployments, thread=True)

    def _authenticate(self):
        try:
            command = CommandDescriptor("auth --open-session")
            self._command_processor.execute_command(command)
        finally:
            self.call_from_thread(self._show_loading_indicator, False)

    def _list_deployments(self):
        try:
            deployments = self._secret_service.get_deployments_page()

            if deployments.get("result") is None:
                return

            deployments_list_view = self.query_one("#deployments", ListView)
            if deployments_list_view.children:
                self.call_from_thread(lambda: deployments_list_view.clear())

            self.call_from_thread(lambda: deployments_list_view.append(DeploymentListHeader()))
            for index, deployment in enumerate(deployments.get("result").get("body")):
                item = DeploymentListItem(deployment)
                if index == 0:
                    item.styles.border_top = ("ascii", self.app.theme_variables["accent"])
                self.call_from_thread(lambda: deployments_list_view.append(item))
        finally:
            self.call_from_thread(self._show_loading_indicator, False)

    def _show_loading_indicator(self, show: bool):
        self.query_one(LoadingIndicator).display = show

    @on(LifecycleOperationModal.Submitted)
    def _handle_lifecycle_operation(self, event: LifecycleOperationModal.Submitted):
        self.pop_screen()
        self.pop_screen()
        self._show_loading_indicator(True)
        self.run_worker(lambda: self._execute_lifecycle_operation(event), thread=True)

    def _execute_lifecycle_operation(self, event: LifecycleOperationModal.Submitted):
        version_segment = f" {event.version}" if event.version and len(event.version) > 0 else ""
        roll_segment = "--roll" if event.roll else ""
        instance_segment = f"--instance {event.instance}" if event.instance and len(event.instance) > 0 else ""

        command = CommandDescriptor(f"{event.operation} {event.deployment_id}{version_segment} {roll_segment}{instance_segment}")

        self._command_processor.execute_command(command)
        self.call_from_thread(self._show_loading_indicator, False)
