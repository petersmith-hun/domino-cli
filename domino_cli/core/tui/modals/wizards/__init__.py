from typing import List

from textual import on
from textual.containers import HorizontalGroup, VerticalGroup, VerticalScroll
from textual.widget import Widget
from textual.widgets import Label, Input, Select, Rule, Switch, TextArea, Button

from domino_cli.core.tui.modals import CustomModalScreen


class BaseWizardModal(CustomModalScreen):

    DEFAULT_CSS = """
        #custom_modal_frame {
            max-width: 90%;
            max-height: 90%;
        }

        .input_name {
            text-style: bold;
            width: 30%;
            padding-top: 1;
        }
        
        .input_row {
            margin-bottom: 1;    
        }
        
        .input_description {
            color: $text-muted;
            text-style: italic;
            width: 100%;
            text-wrap: wrap;
        }
        
        .input_text_input {
            width: 70%;
        }
        
        .extra_padding {
            padding-left: 3;
        }
        
        .input_textarea {
            width: 70%;
            height: 5;
        }

    """

    def __init__(self):
        super().__init__("")

    def _get_content(self) -> List[Widget]:
        return [VerticalScroll(
            *self._add_inputs(),
            self._create_render_button()
        )]

    def _add_inputs(self) -> List[Widget]:
        return []

    def _group(self, title: str, description: str, inputs: List[Widget]) -> List[Widget]:
        return [
            Rule(),
            Label(title, classes="input_title extra_padding"),
            Label(f"ⓘ {description}", classes="input_description extra_padding"),
            Rule(line_style="ascii"),
            *inputs
        ]

    def _select_input(self, input_id: str, title: str, description: str, options: List[tuple[str, str]], disabled: bool = False, control_group: str | None = None) -> VerticalGroup:
        return self._input_frame(title, description, Select(id=input_id, options=options, classes=f"input input_text_input {control_group}", disabled=disabled, allow_blank=False))

    def _text_input(self, input_id: str, title: str, description: str, disabled: bool = False, control_group: str | None = None, default_value: str | None = None) -> VerticalGroup:
        return self._input_frame(title, description, Input(id=input_id, classes=f"input input_text_input {control_group}", disabled=disabled, value=default_value))

    def _textarea_input(self, input_id: str, title: str, description: str, disabled: bool = False, control_group: str | None = None) -> VerticalGroup:
        return self._input_frame(title, description, TextArea(id=input_id, classes=f"input input_textarea {control_group}", disabled=disabled))

    def _switch_input(self, input_id: str, title: str, description: str, disabled: bool = False, control_group: str | None = None, default_value: bool = False) -> VerticalGroup:
        return self._input_frame(title, description, Switch(id=input_id, disabled=disabled, classes=f"input {control_group}", value=default_value))

    def _input_frame(self, title: str, description: str, input_widget: Widget) -> VerticalGroup:
        return VerticalGroup(
            HorizontalGroup(
                Label(title, classes="input_name"),
                input_widget,
            ),
            Label(f"ⓘ {description}", classes="input_description"),
            classes="input_row"
        )

    def _create_render_button(self) -> HorizontalGroup:
        return HorizontalGroup(
            Button("Render configuration", id="render_configuration", variant="primary"),
            classes="full_width align_right"
        )

    def _update_control_group_status(self, selector: str, enabled: bool) -> None:
        for widget in self.query(selector):
            widget.disabled = not enabled

    @on(Button.Pressed, "#render_configuration")
    def _render_configuration(self) -> None:

        responses: dict[str, str | list[str]] = {}
        for input_field in self.query(".input"):

            if input_field.disabled:
                continue

            field_value: str | list[str] | None = None
            if isinstance(input_field, Input):
                field_value = input_field.value
            elif isinstance(input_field, TextArea):
                field_value = [line.strip() for line in input_field.text.split("\n")] if len(input_field.text) > 0 else None
            elif isinstance(input_field, Select):
                field_value = str(input_field.value)
            elif isinstance(input_field, Switch):
                field_value = "yes" if input_field.value else "no"

            if field_value is not None and len(field_value) > 0:
                responses[input_field.id] = field_value

        self._handle_result(responses)

    def _handle_result(self, responses: dict[str, str | list[str]]) -> None:
        pass
