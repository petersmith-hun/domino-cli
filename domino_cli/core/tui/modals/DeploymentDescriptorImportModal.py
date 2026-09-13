from pathlib import Path
from typing import List

from textual import on
from textual.containers import HorizontalGroup
from textual.widget import Widget
from textual.widgets import Label, Button

from domino_cli.core.service.DominoService import DominoService
from domino_cli.core.tui.actions.DeploymentImportActionAdapter import DeploymentImportActionAdapter, \
    DeploymentImportMessage
from domino_cli.core.tui.modals import CustomModalScreen, FilteredDirectoryTree


class DeploymentDescriptorImportModal(CustomModalScreen):
    """
    TODO.
    """

    DEFAULT_CSS = """
    #custom_modal_frame {
        width: 60%;
        height: 60%;
    }
    """

    def __init__(self, domino_service: DominoService):
        super().__init__("")
        self._domino_service = domino_service
        self._deployment_import_action_adapter = DeploymentImportActionAdapter(self.app, self._domino_service)
        self._path: Path | None = None

    def _get_title(self) -> Label:
        return Label(f"Import deployment descriptor")

    def _get_content(self) -> List[Widget]: # TODO modal is not responsive yet (I guess the same applies to the OAuth import modal)
        return [
            FilteredDirectoryTree(),
            Label("❌ No file has been selected yet", id="file_selection_indicator", classes="mt2"),
            HorizontalGroup(
                Button("OK", id="import_deployment_descriptor", variant="primary", classes="ml2"),
                classes="align_right full_width mt2",
            ),
        ]

    def on_directory_tree_file_selected(self, event: FilteredDirectoryTree.FileSelected):
        self._path = event.path
        self.query_one("#file_selection_indicator", Label).update(f"✔ File selected: {event.path}")

    @on(Button.Pressed)
    def _handle_lifecycle_operation(self):

        deployment_import_message = DeploymentImportMessage(file_path=str(self._path))

        self.app.pop_screen()
        self._deployment_import_action_adapter.execute(deployment_import_message)
