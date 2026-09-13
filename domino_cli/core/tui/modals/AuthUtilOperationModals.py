import os
from typing import Any

from textual import on
from textual.containers import HorizontalGroup, VerticalScroll
from textual.widget import Widget
from textual.widgets import Label, Input, TextArea, Button

from domino_cli.core.domain.AuthMode import AuthMode
from domino_cli.core.domain.CustomExceptions import AuthenticationException
from domino_cli.core.service.AuthenticationService import AuthenticationService
from domino_cli.core.tui.modals import CustomModalScreen


class PasswordEncryptionModal(CustomModalScreen):

    DEFAULT_CSS = """
    #custom_modal_frame {
        width: 60%;
        height: 60%;
    }
    """

    def __init__(self, authentication_service: AuthenticationService):
        super().__init__("")
        self._authentication_service = authentication_service

    def _get_title(self) -> Label:
        return Label("Password Encryption")

    def _get_sub_title(self) -> Label:
        return Label("ⓘ This utility encrypts passwords using bcrypt, that can be used as a Domino direct auth password")

    def _get_content(self) -> list[Widget]:
        return [
            Input(placeholder="Enter password to be encrypted", id="password", classes="full_width"),
            TextArea(id="encrypted_password", placeholder="You'll get the encrypted password here.", classes="full_width mt2 h4", read_only=True),
            HorizontalGroup(
                Button("Encrypt", id="encrypt_button", variant="primary"),
                classes="align_right mt2"
            )
        ]

    @on(Button.Pressed)
    def _handle_encrypt_button(self):
        password = self.query_one("#password", Input).value
        encrypted_password = self._authentication_service.encrypt_password(password)
        self.query_one("#encrypted_password", TextArea).load_text(encrypted_password)


class GenerateAccessTokenModal(CustomModalScreen):

    DEFAULT_CSS = """
    #custom_modal_frame {
        width: 60%;
        height: 60%;
    }
    """

    def __init__(self, authentication_service: AuthenticationService):
        super().__init__("")
        self._authentication_service = authentication_service

    def _get_title(self) -> Label:
        return Label("Generated access token")

    def _get_sub_title(self) -> Label:
        return Label("ⓘ The generated access token can be used to authenticate with Domino's API")

    def _get_content(self) -> list[Widget]:
        return [
            TextArea(id="access_token", placeholder="You'll get the generated token here.", classes="full_width mt2 h12", read_only=True),
            HorizontalGroup(
                Button("Generate token", id="generate_token", variant="primary"),
                classes="align_right mt2"
            )
        ]

    @on(Button.Pressed)
    def _handle_generate_access_token(self):
        self.set_loading(True)
        self.run_worker(self._request_access_token, thread=True)

    def _request_access_token(self):

        try:
            access_token = self._authentication_service.generate_token()
            self.app.call_from_thread(self.set_loading, False)
            self.app.call_from_thread(lambda: self.query_one("#access_token", TextArea).load_text(access_token))

        except AuthenticationException as exc:
            self.app.call_from_thread(self.set_loading, False)
            self.app.call_from_thread(lambda: self.app.notify(str(exc), title="Authentication failed", severity="error"))


class SetAuthModeModal(CustomModalScreen):

    DEFAULT_CSS = """
    #custom_modal_frame {
        width: 60%;
        height: 70%;
    }
    
    .input_label {
        width: 25;
        padding-top: 1;
    }
    
    .mb2 {
        margin-bottom: 2;
    }
    """

    def __init__(self, authentication_service: AuthenticationService):
        super().__init__("")
        self._authentication_service = authentication_service

    def _get_title(self) -> Label:
        return Label("Set authentication mode")

    def _get_sub_title(self) -> Label:
        return Label("ⓘ This utility changes the active authentication mode between direct and OAuth authentication")

    def _get_content(self) -> list[Widget]:

        current_auth_mode = self._authentication_service.get_auth_mode()
        target_auth_mode = self._get_target_auth_mode()

        auth_mode_input_group = [
            Label(f"Current authentication mode: {current_auth_mode.value}", id="current_auth_mode",
                  classes="full_width"),
            HorizontalGroup(
                Button(f"Switch to {target_auth_mode.value} auth", id="set_auth_mode", variant="primary"),
                classes="align_right mt2 mb2"
            )
        ]

        direct_mode_parameters = []
        if current_auth_mode == AuthMode.DIRECT:
            direct_mode_parameters = [
                self._create_input("Username", "DOMINO_CLI_USERNAME"),
                self._create_input("Password", "DOMINO_CLI_PASSWORD", password=True),
            ]

        oauth_mode_parameters = []
        if current_auth_mode == AuthMode.OAUTH:
            oauth_mode_parameters = [
                self._create_input("Token exchange URL", "DOMINO_OAUTH_TOKEN_URL"),
                self._create_input("Client ID", "DOMINO_OAUTH_CLIENT_ID"),
                self._create_input("Client Secret", "DOMINO_OAUTH_CLIENT_SECRET", password=True),
                self._create_input("Scope", "DOMINO_OAUTH_SCOPE"),
                self._create_input("Audience", "DOMINO_OAUTH_AUDIENCE"),
            ]

        return [
            VerticalScroll(
                *auth_mode_input_group,
                *direct_mode_parameters,
                *oauth_mode_parameters,
                HorizontalGroup(
                    Button("Update configuration", id="update_auth_config", variant="primary"),
                    classes="align_right mt2"
                )
            )
        ]

    @on(Button.Pressed, selector="#set_auth_mode")
    def _switch_auth_mode(self):
        self._authentication_service.set_mode(self._get_target_auth_mode().value)
        self.refresh(self.region, recompose=True)

    @on(Button.Pressed, selector="#update_auth_config")
    def _update_auth_config(self):

        for auth_param_input in self.query(Input).results():
            if auth_param_input.disabled:
                continue

            os.environ[str(auth_param_input.id)] = auth_param_input.value

        self.refresh(self.region, recompose=True)

    def _create_input(self, label: str, env_key: str, password: bool = False, placeholder_override: str | None = None) -> HorizontalGroup:

        placeholder = placeholder_override if placeholder_override else f"Enter your {label}"

        return HorizontalGroup(
            Label(label, classes="input_label"),
            Input(id=env_key, placeholder=placeholder, password=password, **self._getenv(env_key))
        )

    def _get_target_auth_mode(self) -> AuthMode:
        current_auth_mode = self._authentication_service.get_auth_mode()
        return AuthMode.DIRECT \
            if current_auth_mode == AuthMode.OAUTH \
            else AuthMode.OAUTH

    def _getenv(self, key: str) -> dict[str, Any]:

        value = os.getenv(key)
        return { "value": value, "disabled": value is not None }

