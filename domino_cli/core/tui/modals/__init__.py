from pathlib import Path
from typing import List, Iterable, Callable

from textual import on, events
from textual.app import ComposeResult
from textual.containers import Vertical, VerticalGroup, HorizontalGroup, VerticalScroll
from textual.screen import ModalScreen
from textual.widget import Widget
from textual.widgets import Rule, Footer, Label, DirectoryTree, Button


class CustomModalScreen(ModalScreen):

    BINDINGS = [
        ("x", "app.pop_screen", "Close")
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
            padding-top: 1;
        }
        
        #custom_modal_controls {
            padding: 0 3;
            outline-left: ascii $accent;
            outline-right: ascii $accent;
        }
        
        .mt2 {
            margin-top: 2;
        }
        
        .ml2 {
            margin-left: 2;
        }
        
        .h4 {
            height: 4;
        }
        
        .mh12 {
            max-height: 12;
        }
        
        .full_width {
            width: 100%;
        }
        
        .align_right {
            align-horizontal: right;
        }
        """

    def __init__(self):
        super().__init__()

    def compose(self) -> ComposeResult:

        sub_title = self._get_sub_title()

        with Vertical(id="custom_modal_frame"):
            with VerticalGroup(id="custom_modal_controls"):
                yield self._get_title()
                if sub_title:
                    yield sub_title
                yield Rule()
                with VerticalScroll(id="custom_modal_content_scroll"):
                    for widget in self._get_content():
                        yield widget
            yield Footer(id="custom_modal_footer")

    def _on_mount(self, event: events.Mount) -> None:

        inputs = self.query(".input")
        if len(inputs) > 0:
            inputs[0].focus()

    def _get_title(self) -> Label:
        pass

    def _get_sub_title(self) -> Label:
        pass

    def _get_content(self) -> List[Widget]:
        pass


class FilteredDirectoryTree(DirectoryTree):
    def __init__(self):
        super().__init__("./", id="file_picker", classes="mh12 full_width")

    def filter_paths(self, paths: Iterable[Path]):
        return [path for path in paths if path.is_dir() or path.name.endswith(".yml") or path.name.endswith(".yaml")]


class ConfirmationModal(CustomModalScreen):
    DEFAULT_CSS = """
        #custom_modal_frame {
            max-width: 80;
            max-height: 20;
        }
    """

    def __init__(self, confirmation_text: str, callback: Callable[[], None]):
        super().__init__()
        self._confirmation_text = confirmation_text
        self._callback = callback

    def _get_title(self) -> Label:
        return Label("Are you sure you want to continue?")

    def _get_sub_title(self) -> Label:
        return Label(self._confirmation_text)

    def _get_content(self) -> List[Widget]:
        return [
            HorizontalGroup(
                Button("Cancel", id="cancel_button"),
                Button("OK", id="confirmation_button", classes="ml2", variant="warning"),
                classes="full_width align_right"
            )
        ]

    @on(Button.Pressed, "#confirmation_button")
    def _handle_confirmation(self):
        self.dismiss()
        self.dismiss()
        self._callback()

    @on(Button.Pressed, "#cancel_button")
    def _handle_cancel(self):
        self.dismiss()
