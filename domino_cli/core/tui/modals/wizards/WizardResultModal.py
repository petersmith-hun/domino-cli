import os
from enum import Enum
from typing import List

import pyperclip
from textual import on
from textual.containers import HorizontalGroup
from textual.widget import Widget
from textual.widgets import Label, TextArea, Button, Input

from domino_cli.core.tui.modals.wizards import BaseWizardModal


class ConfigType(Enum):
    DEPLOYMENT = ("Deployment", "./deployment.yml")
    COORDINATOR = ("Coordinator", "./coordinator_production.yml")
    DOCKER_AGENT = ("Docker Agent", "./docker_agent_production.yml")
    BINARY_EXECUTABLE = ("Binary Executable Agent", "./binary_executable_agent_production.yml")


class WizardResultModal(BaseWizardModal):

    DEFAULT_CSS = """
        #custom_modal_frame {
            max-width: 80%;
            max-height: 80%;
        }
    """

    BINDINGS = [
        ("c", "copy_result", "Copy config to clipboard")
    ]

    def __init__(self, config_type: ConfigType, yaml_content: str):
        super().__init__()
        self._config_type = config_type
        self._yaml_content = yaml_content

    def _get_title(self) -> Label:
        return Label(self._config_type.value[0])

    def _get_content(self) -> List[Widget]:
        return [
            TextArea(text=self._yaml_content, read_only=True, language="yaml"),
            self._text_input("target_file_path", "Target file path", "Please enter the target file path to save the configuration into a YAML file",
                             default_value=self._config_type.value[1]),
            HorizontalGroup(
                Button("Save", id="save_configuration", variant="primary"),
                classes="full_width align_right"
            )
        ]

    @on(Button.Pressed, "#save_configuration")
    def _handle_save(self) -> None:
        self.dismiss()
        self.dismiss()
        target_file_path = self.query_one("#target_file_path", Input).value
        try:
            with open(target_file_path, "w") as file:
                file.write(self._yaml_content)
                absolute_path = os.path.realpath(file.name)
                self.app.notify(f"Configuration saved successfully to file {absolute_path}", title="Configuration save", severity="information")

        except Exception as exc:
            self.app.notify(f"Failed to save the configuration file: {exc}", title="Configuration save", severity="error")

    def action_copy_result(self) -> None:

        pyperclip.copy(self._yaml_content)
        self.app.notify("Configuration has been copied to clipboard", title="Copy successful", severity="information")
