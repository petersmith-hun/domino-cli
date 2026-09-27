from typing import List

from textual.widgets import Label

from domino_cli.core.service.AuthenticationService import AuthenticationService
from domino_cli.core.tui.modals import CustomModalListItem, OptionsModalScreen
from domino_cli.core.tui.modals.AuthUtilOperationModals import PasswordEncryptionModal, GenerateAccessTokenModal, \
    SetAuthModeModal


class AuthUtilOptionsModal(OptionsModalScreen):

    def __init__(self, authentication_service: AuthenticationService):
        super().__init__()
        self._authentication_service = authentication_service

    def _get_title(self) -> Label:
        return Label("Authentication utilities")

    def _get_items(self) -> List[CustomModalListItem]:

        return [
            CustomModalListItem("encrypt_password", "Encrypt password",
                                "This utility encrypts passwords using bcrypt, that can be used as a Domino direct auth password"),
            CustomModalListItem("generate_token", "Generate access token",
                                "The generated access token can be used to authenticate with Domino's API"),
            CustomModalListItem("set_auth_mode", "Set authentication mode",
                                "This utility changes the active authentication mode between direct and OAuth authentication")
        ]

    def _on_option_selected(self, item_id: str) -> None:

        if item_id == "encrypt_password":
            self.app.push_screen(PasswordEncryptionModal(self._authentication_service))
        elif item_id == "generate_token":
            self.app.push_screen(GenerateAccessTokenModal(self._authentication_service))
        elif item_id == "set_auth_mode":
            self.app.push_screen(SetAuthModeModal(self._authentication_service))
