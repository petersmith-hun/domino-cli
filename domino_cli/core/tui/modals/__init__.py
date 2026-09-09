from pathlib import Path
from typing import List, Iterable

from textual.app import ComposeResult
from textual.containers import Vertical, VerticalGroup
from textual.screen import ModalScreen
from textual.widget import Widget
from textual.widgets import Rule, Footer, Label, DirectoryTree


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
        
        .mt2 {
            margin-top: 2;
        }
        
        .ml2 {
            margin-left: 2;
        }
        
        .h12 {
            height: 12;
        }
        
        .full_width {
            width: 100%;
        }
        
        .align_right {
            align-horizontal: right;
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

    def _get_content(self) -> List[Widget]:
        pass


class FilteredDirectoryTree(DirectoryTree):
    """
    TODO.
    """
    def __init__(self):
        super().__init__("./", id="file_picker", classes="mt2 h12 full_width")

    def filter_paths(self, paths: Iterable[Path]):
        return [path for path in paths if path.is_dir() or path.name.endswith(".yml") or path.name.endswith(".yaml")]
