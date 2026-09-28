from pathlib import Path
from typing import List, Iterable, Callable

from textual import on, events
from textual.app import ComposeResult
from textual.containers import Vertical, VerticalGroup, HorizontalGroup, VerticalScroll
from textual.events import Mount
from textual.screen import ModalScreen
from textual.widget import Widget
from textual.widgets import Rule, Footer, Label, DirectoryTree, Button, ListItem, ListView


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


class CustomModalListItem(ListItem):

    DEFAULT_CSS = """
        CustomModalListItem {
            padding: 1 3;
            outline-left: ascii $accent;
            outline-right: ascii $accent;
        }
    
        .item_name {
            text-style: bold;
        }
        
        .item_description {
            color: $text-muted;
            text-style: italic;
        }
    """

    def __init__(self, item_id: str, name: str, description: str):
        super().__init__(VerticalGroup(
            Label(name, classes="item_name"),
            Label(f"ⓘ {description}", classes="item_description")
        ))
        self.item_id = item_id


class CustomModalOptionList(ListView):

    DEFAULT_CSS = """
        CustomModalOptionList {
            outline-left: ascii $accent;
            outline-right: ascii $accent;
            margin-bottom: 0;
            padding-bottom: 0;
        }
    """
    def __init__(self, callback: Callable[[str], None], *items):
        super().__init__(*items)
        self._callback = callback

    def _on_mount(self, _: Mount) -> None:
        self.focus()

    def action_select_cursor(self) -> None:

        if self.highlighted_child is None or not isinstance(self.highlighted_child, CustomModalListItem):
            return

        self._callback(self.highlighted_child.item_id)


class OptionsModalScreen(ModalScreen):

    BINDINGS = [
        ("x", "app.pop_screen", "Close")
    ]

    DEFAULT_CSS = """
        OptionsModalScreen {
            align: center middle;
        }
        
        ListView {
            outline-left: ascii $accent;
            outline-right: ascii $accent;
            margin-bottom: 0;
            padding-bottom: 0;
        }
        
        VerticalScroll {
            outline-left: ascii $accent;
            outline-right: ascii $accent;
            scrollbar-size-vertical: 0;
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
    """

    def compose(self) -> ComposeResult:

        sub_title = self._get_sub_title()

        with Vertical(id="custom_modal_frame"):
            with VerticalGroup(id="custom_modal_controls"):
                yield self._get_title()
                if sub_title:
                    yield sub_title
                yield Rule()
            with VerticalScroll(id="custom_modal_content_scroll"):
                yield CustomModalOptionList(self._on_option_selected, *self._get_items())
            yield Footer(id="custom_modal_footer")

    def _on_option_selected(self, item_id: str) -> None:
        pass

    def _get_title(self) -> Label:
        pass

    def _get_sub_title(self) -> Label:
        pass

    def _get_items(self) -> List[CustomModalListItem]:
        pass
