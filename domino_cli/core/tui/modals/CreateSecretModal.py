from typing import List

from textual import on
from textual.containers import HorizontalGroup
from textual.widget import Widget
from textual.widgets import Label, Input, Button

from domino_cli.core.service.SecretService import SecretService
from domino_cli.core.tui.actions.CreateSecretActionAdapter import CreateSecretActionAdapter, NewSecret
from domino_cli.core.tui.modals import CustomModalScreen


class CreateSecretModal(CustomModalScreen):

    DEFAULT_CSS = """
        #custom_modal_frame {
            max-width: 180;
            max-height: 30;
        }
        
        .input_label {
            width: 40;
            margin-right: 2;
            padding-top: 1;
            text-align: right;
        }
        
        .mt1 {
            margin-top: 1;
        }
    """

    def __init__(self, secret_service: SecretService):
        super().__init__()
        self._secret_service = secret_service
        self._create_secret_action_adapter = CreateSecretActionAdapter(self.app, self._secret_service)

    def _get_title(self) -> Label:
        return Label("Create secret")

    def _get_content(self) -> List[Widget]:
        return [
            self._create_input("secret_context", "Secret context"),
            self._create_input("secret_key", "Secret key"),
            self._create_input("secret_value", "Secret value", password=True),
            HorizontalGroup(
                Button("Create secret", id="create_secret_button", variant="primary")
                , classes="mt2 align_right"
            )
        ]

    @on(Button.Pressed, "#create_secret_button")
    def _handle_secret_creation(self):

        event = NewSecret(
            secret_context=self._get_input_value("secret_context"),
            secret_key=self._get_input_value("secret_key"),
            secret_value=self._get_input_value("secret_value")
        )

        self.dismiss()
        self._create_secret_action_adapter.execute(event)

    def _get_input_value(self, input_id: str) -> str:
        return self.query_one(f"#{input_id}", Input).value

    @staticmethod
    def _create_input(input_id: str, input_label: str, password: bool = False) -> HorizontalGroup:
        return HorizontalGroup(
            Label(input_label, classes="input_label"),
            Input(id=input_id, password=password),
            classes="mt1"
        )
