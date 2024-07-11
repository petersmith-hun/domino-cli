from typing import List, Dict

from domino_cli.core.domain.AuthMode import AuthMode
from domino_cli.core.domain.SessionContext import SessionContext
from domino_cli.core.service.SessionContextHolder import SessionContextHolder
from domino_cli.core.service.auth.AbstractAuthHandler import AbstractAuthHandler
from domino_cli.core.service.auth.AuthUtils import AuthUtils
from domino_cli.core.service.utility.BCryptUtil import encrypt


class AuthenticationService:
    """
    Service implementation for handling authentication related operations.
    """
    def __init__(self, default_auth_mode: AuthMode, session_context_holder: SessionContextHolder,
                 auth_handlers: List[AbstractAuthHandler]):
        self._auth_mode: AuthMode = default_auth_mode
        self._session_context_holder: SessionContextHolder = session_context_holder
        self._auth_handler_dict: Dict[AuthMode, AbstractAuthHandler] = self._init_handler_map(auth_handlers)

        print(f"Domino authentication mode is set to {self._auth_mode.name}. Use 'auth --set-mode' command to change")

    def encrypt_password(self) -> None:
        """
        Utility to encrypt a password with BCrypt for usage in Domino (as service user password).
        """
        encrypted_password: str = encrypt(AuthUtils.input_password())

        print("Encrypted password: {0}".format(encrypted_password))

    def generate_token(self) -> None:
        """
        Utility to generate a Domino authentication token for usage by external services (eg. Jenkins).
        """
        try:
            session_context: SessionContext = self._request_token()

            print("Generated auth token: {0}".format(session_context.authentication_token))
        except Exception as exc:
            print("Failed to generate token - reason: {0}".format(str(exc)))

    def open_session(self) -> None:
        """
        Opens an authenticated session for Domino CLI.
        This step is required before executing any lifecycle command, otherwise Domino rejects every request.
        """
        try:
            session_context: SessionContext = self._request_token()
            self._session_context_holder.update(session_context)

            print("Session is open")
        except Exception as exc:
            print("Failed to open session - reason: {0}".format(str(exc)))

    def set_mode(self, new_mode: str) -> None:
        """
        Changes the currently set authentication mode to the specified one.
        The accepted values are the ones defined in the AuthMode enum (currently 'direct' and 'oauth').

        :param new_mode: authentication mode to change to
        """
        try:
            self._auth_mode = AuthMode.by_value(new_mode)
        except KeyError:
            print(f"Failed to change authentication mode, invalid mode defined: {new_mode}")

    def _request_token(self) -> SessionContext:

        return self._auth_handler_dict[self._auth_mode] \
            .create_session_context()

    @staticmethod
    def _init_handler_map(auth_handlers):
        return {handler.for_auth_mode(): handler for handler in auth_handlers}

