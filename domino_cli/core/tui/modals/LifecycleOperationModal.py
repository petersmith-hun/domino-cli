from typing import List
from typing import Literal

from textual import on
from textual.containers import HorizontalGroup, VerticalGroup
from textual.widget import Widget
from textual.widgets import Label, Input, Checkbox, Button

from domino_cli.core.service.DominoService import DominoService
from domino_cli.core.tui.actions.LifecycleOperationActionAdapter import LifecycleOperationActionAdapter, \
    LifecycleMessage
from domino_cli.core.tui.modals import CustomModalScreen


class LifecycleOperationModal(CustomModalScreen):

    DEFAULT_CSS = """
        #custom_modal_frame {
            max-width: 50;
            max-height: 30;
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

    def __init__(self, domino_service: DominoService, deployment_id: str, operation: Literal["deploy_latest", "deploy_version", "start", "stop", "restart", "info"]):
        super().__init__(deployment_id)
        self._domino_service = domino_service
        self._operation = operation
        self._lifecycle_operation_action_adapter = LifecycleOperationActionAdapter(self.app, self._domino_service)

    def _get_title(self) -> Label:
        return Label(f"{self._SYMBOL_MAP.get(self._operation)} {self._operation} {self._deployment_id}")

    def _get_content(self) -> List[Widget]:

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
            widgets.append(Checkbox("Roll all instances", id="roll", classes="full_width mt2"))

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

        lifecycle_message = LifecycleMessage(
            operation=self._operation,
            deployment_id=self._deployment_id,
            roll=roll_checkbox.value if isinstance(roll_checkbox, Checkbox) else False,
            instance=self.query_one("#instance_suffix", Input).value,
            version=version_input.value if isinstance(version_input, Input) else None,
        )

        self.app.pop_screen()
        self.app.pop_screen()
        self._lifecycle_operation_action_adapter.execute(lifecycle_message)
