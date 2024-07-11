from requests import Response

from domino_cli.core.client.OAuthAuthorizationClient import OAuthAuthorizationClient
from domino_cli.core.domain.AuthMode import AuthMode
from domino_cli.core.domain.OAuthConfig import OAuthConfig
from domino_cli.core.domain.SessionContext import SessionContext
from domino_cli.core.service.auth.AbstractAuthHandler import AbstractAuthHandler


class OAuthAuthHandler(AbstractAuthHandler):
    """
    AbstractAuthHandler implementation utilizing an external, OAuth 2.0 compliant authorization server.
    Authorization request will be sent as a Client Credentials Grant Flow request.
    """
    def __init__(self, oauth_config: OAuthConfig, oauth_authorization_client: OAuthAuthorizationClient):
        self._oauth_config = oauth_config
        self._oauth_authorization_client = oauth_authorization_client

    def create_session_context(self) -> SessionContext:

        if not self._oauth_config.is_configured():
            raise Exception("Insufficient configuration for OAuth authorization - please check the notes above")

        response: Response = self._oauth_authorization_client.request_authorization()

        if not response.status_code == 200:
            raise Exception("Failed to authenticate - OAuth Authorization Server responded with {0}".format(response.status_code))

        return SessionContext(self._oauth_config.client_id, response.json()["access_token"])

    def for_auth_mode(self) -> AuthMode:
        return AuthMode.OAUTH
