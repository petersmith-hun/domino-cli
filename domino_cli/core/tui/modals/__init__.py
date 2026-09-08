from typing import List

from textual.app import ComposeResult
from textual.containers import Vertical, VerticalGroup
from textual.screen import ModalScreen
from textual.widget import Widget
from textual.widgets import Rule, Footer, Label


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

    def _get_content(self) -> List[Widget]:
        pass
