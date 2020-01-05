import os
from getpass import getpass

import bcrypt
from requests import Response

from core.client.DominoClient import DominoClient
from core.domain.AuthRequest import AuthRequest
from core.domain.DominoRequest import DominoRequest
from core.domain.HTTPMethod import HTTPMethod
from core.domain.SessionContext import SessionContext
from core.service.SessionContextHolder import SessionContextHolder

_PASSWORD_ENCODING = "utf8"
_DOMINO_CLI_USERNAME = "DOMINO_CLI_USERNAME"
_DOMINO_CLI_PASSWORD = "DOMINO_CLI_PASSWORD"


class AuthenticationService:
    """
    Service implementation for handling authentication related operations.
    """
    def __init__(self, domino_client: DominoClient, session_context_holder: SessionContextHolder):
        self._domino_client = domino_client
        self._session_context_holder = session_context_holder

    def encrypt_password(self) -> None:
        """
        Utility to encrypt a password with BCrypt for usage in Domino (as service user password).
        """
        plain_password: bytes = self._input_password().encode(_PASSWORD_ENCODING)
        encrypted_password_as_byte_array: bytearray = bcrypt.hashpw(plain_password, bcrypt.gensalt())
        encrypted_password: str = encrypted_password_as_byte_array.decode(_PASSWORD_ENCODING)

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

    def _request_token(self) -> SessionContext:

        auth_request = self._generate_auth_request()

        return self._authenticate_with_domino(auth_request)

    def _generate_auth_request(self) -> AuthRequest:

        username: str = self._input_username()
        password: str = self._input_password()

        return AuthRequest(username, password)

    def _authenticate_with_domino(self, auth_request: AuthRequest) -> SessionContext:

        domino_request: DominoRequest = DominoRequest(HTTPMethod.POST, "/claim-token", body=auth_request.get_as_dict())
        response: Response = self._domino_client.send_command(domino_request)

        if not response.status_code == 201:
            raise Exception("Failed to authenticate - Domino responded with {0}".format(response.status_code))

        return SessionContext(auth_request.username, response.json()["jwt"])

    def _input_username(self) -> str:

        username = os.getenv(_DOMINO_CLI_USERNAME)
        if username is None:
            username = input(" ** specify username: ")

        return username

    def _input_password(self) -> str:

        password = os.getenv(_DOMINO_CLI_PASSWORD)
        if password is None:
            password = getpass(" ** specify password: ")

        return password
