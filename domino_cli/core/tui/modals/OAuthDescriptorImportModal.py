from pathlib import Path
from typing import List

from textual import on
from textual.containers import HorizontalGroup
from textual.widget import Widget
from textual.widgets import Label, Checkbox, Button

from domino_cli.core.service.DominoService import DominoService
from domino_cli.core.tui.actions.OAuthImportActionAdapter import OAuthImportActionAdapter, OAuthImportMessage
from domino_cli.core.tui.modals import CustomModalScreen, FilteredDirectoryTree


class OAuthDescriptorImportModal(CustomModalScreen):

    DEFAULT_CSS = """
    #custom_modal_frame {
        max-width: 90%;
        max-height: 90%;
    }
    """

    def __init__(self, domino_service: DominoService, deployment_id: str):
        super().__init__()
        self._deployment_id = deployment_id
        self._domino_service = domino_service
        self._oauth_import_action_adapter = OAuthImportActionAdapter(self.app, self._domino_service)
        self._path: Path | None = None

    def _get_title(self) -> Label:
        return Label(f"Import OAuth descriptor for {self._deployment_id}")

    def _get_content(self) -> List[Widget]:
        return [
            FilteredDirectoryTree(),
            Label("❌ No file has been selected yet", id="file_selection_indicator", classes="mt2"),
            HorizontalGroup(
                Checkbox("Dry-run", id="dry_run"),
                Button("OK", id="import_oauth_descriptor", variant="primary", classes="ml2"),
                classes="align_right full_width mt2",
            ),
        ]

    def on_directory_tree_file_selected(self, event: FilteredDirectoryTree.FileSelected):
        self._path = event.path
        self.query_one("#file_selection_indicator", Label).update(f"✔ File selected: {event.path}")

    @on(Button.Pressed)
    def _handle_lifecycle_operation(self):

        oauth_import_message = OAuthImportMessage(
            deployment_id=self._deployment_id,
            dry_run=self.query_one("#dry_run", Checkbox).value,
            file_path=str(self._path)
        )

        self.app.pop_screen()
        self.app.pop_screen()
        self._oauth_import_action_adapter.execute(oauth_import_message)
