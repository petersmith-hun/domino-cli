from typing import List

import pyperclip
from textual.containers import HorizontalGroup
from textual.widget import Widget
from textual.widgets import Label

from domino_cli.core.tui.modals import CustomModalScreen


class RetrievedSecretsModal(CustomModalScreen):

    DEFAULT_CSS = """
        #custom_modal_frame {
            max-width: 180;
            max-height: 20;
        }
        
        .secret_key {
            width: 80;
            text-align: right;
            margin-right: 2;
            
        }
        
        .secret_line {
            border-bottom: ascii $accent;
        }
        
        .secret_value {
            text-style: italic;
        }
    """

    BINDINGS = [
        ("c", "copy_result", "Copy retrieved secret(s) to clipboard")
    ]

    def __init__(self, retrieved_secrets: dict[str, str]):
        super().__init__()
        self.retrieved_secrets = retrieved_secrets

    def _get_title(self) -> Label:
        return Label("Retrieved Secrets")

    def _get_content(self) -> List[Widget]:
        return [HorizontalGroup(Label(key, classes="secret_key"), Label(value, classes="secret_value"), classes="secret_line")
                for key, value
                in self.retrieved_secrets.items()]

    def action_copy_result(self) -> None:

        secrets = "\n".join([f"{key}={value}" for key, value in self.retrieved_secrets.items()])

        pyperclip.copy(secrets)
        self.app.notify("Retrieved secrets has been copied to clipboard in env file format", title="Copy successful", severity="information")
