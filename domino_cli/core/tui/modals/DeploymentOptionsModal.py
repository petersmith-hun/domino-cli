from typing import List

from textual.widget import Widget
from textual.widgets import Label, OptionList
from textual.widgets.option_list import Option

from domino_cli.core.service.CommandProcessor import CommandProcessor
from domino_cli.core.tui.modals import CustomModalScreen
from domino_cli.core.tui.modals.LifecycleOperationModal import LifecycleOperationModal


class DeploymentOptionsModal(CustomModalScreen):
    """
    TODO.
    """
    def __init__(self, command_processor: CommandProcessor, deployment_id: str):
        super().__init__(deployment_id)
        self._command_processor = command_processor

    def _get_title(self) -> Label:
        return Label(f"{self._deployment_id} lifecycle operations")

    def _get_content(self) -> List[Widget]:
        return [
            DeploymentOptionList(self._command_processor, self._deployment_id)
        ]


class DeploymentOptionList(OptionList):
    """
    TODO.
    """
    def __init__(self, command_processor: CommandProcessor, deployment_id: str):
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
        self._command_processor = command_processor


    def action_select(self) -> None:

        if self.highlighted_option is None:
            return

        option_id = self.highlighted_option.id

        if option_id in ["deploy_latest", "deploy_version", "start", "restart", "stop", "info"]:
            self.app.push_screen(LifecycleOperationModal(self._command_processor, self._deployment_id, operation=option_id))
