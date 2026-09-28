from requests import Response

from domino_cli.core.client.DominoClient import DominoClient
from domino_cli.core.domain.AuthMode import AuthMode
from domino_cli.core.domain.AuthRequest import AuthRequest
from domino_cli.core.domain.DominoRequest import DominoRequest
from domino_cli.core.domain.HTTPMethod import HTTPMethod
from domino_cli.core.domain.SessionContext import SessionContext
from domino_cli.core.service.auth import parse_token_expiration
from domino_cli.core.service.auth.AbstractAuthHandler import AbstractAuthHandler
from domino_cli.core.service.auth.AuthUtils import AuthUtils


class DirectAuthHandler(AbstractAuthHandler):
    """
    AbstractAuthHandler implementation using the legacy authentication flow of Domino. Request is sent directly to
    Domino, calling the /claim-token endpoint. Therefore, this mode requires Domino to be properly configured
    regarding authentication (having the administrative user set up in Domino's config).
    """
    def __init__(self, domino_client: DominoClient):
        self._domino_client = domino_client

    def create_session_context(self) -> SessionContext:

        auth_request = self._generate_auth_request()

        return self._authenticate_with_domino(auth_request)

    def for_auth_mode(self) -> AuthMode:
        return AuthMode.DIRECT

    @staticmethod
    def _generate_auth_request() -> AuthRequest:

        username: str = AuthUtils.input_username()
        password: str = AuthUtils.input_password()

        return AuthRequest(username, password)

    def _authenticate_with_domino(self, auth_request: AuthRequest) -> SessionContext:

        domino_request: DominoRequest = DominoRequest(HTTPMethod.POST, "/claim-token", body=auth_request.get_as_dict())
        response: Response = self._domino_client.send_command(domino_request)

        if not response.status_code == 201:
            raise Exception("Failed to authenticate - Domino responded with {0}".format(response.status_code))

        token_response = response.json()
        expires_at = parse_token_expiration(token_response["jwt"])

        return SessionContext(auth_request.username, token_response["jwt"], expires_at)
