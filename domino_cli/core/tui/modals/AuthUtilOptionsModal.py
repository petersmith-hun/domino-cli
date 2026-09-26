from typing import List

from textual.widget import Widget
from textual.widgets import Label, OptionList
from textual.widgets.option_list import Option

from domino_cli.core.service.AuthenticationService import AuthenticationService
from domino_cli.core.tui.modals import CustomModalScreen
from domino_cli.core.tui.modals.AuthUtilOperationModals import PasswordEncryptionModal, GenerateAccessTokenModal, \
    SetAuthModeModal


class AuthUtilOptionsModal(CustomModalScreen):

    def __init__(self, authentication_service: AuthenticationService):
        super().__init__()
        self._authentication_service = authentication_service

    def _get_title(self) -> Label:
        return Label("Authentication utilities")

    def _get_content(self) -> List[Widget]:
        return [
            AuthUtilsOptionList(self._authentication_service)
        ]


class AuthUtilsOptionList(OptionList):

    def __init__(self, authentication_service: AuthenticationService):
        super().__init__(
            Option("Encrypt password", id="encrypt_password"),
            Option("Generate access token", id="generate_token"),
            Option("Set authentication mode", id="set_auth_mode")
        )
        self._authentication_service = authentication_service

    def action_select(self) -> None:

        if self.highlighted_option is None:
            return

        selected_option = self.highlighted_option.id

        if selected_option == "encrypt_password":
            self.app.push_screen(PasswordEncryptionModal(self._authentication_service))
        elif selected_option == "generate_token":
            self.app.push_screen(GenerateAccessTokenModal(self._authentication_service))
        elif selected_option == "set_auth_mode":
            self.app.push_screen(SetAuthModeModal(self._authentication_service))
