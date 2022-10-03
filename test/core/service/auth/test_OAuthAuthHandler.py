from __future__ import annotations
from unittest import TestCase, mock

from requests import Response

from core.client.OAuthAuthorizationClient import OAuthAuthorizationClient
from core.domain.AuthMode import AuthMode
from core.domain.OAuthConfig import OAuthConfig
from core.domain.SessionContext import SessionContext
from core.service.auth.OAuthAuthHandler import OAuthAuthHandler

_TOKEN_URL = "http://localhost:9999/token"
_CLIENT_ID = "domino-cli-1"
_CLIENT_SECRET = "domino1234"
_SCOPE = "read:info"
_AUDIENCE = "aud:domino"
_JWT_TOKEN = "jwt_token"


def _getenv_side_effect(parameter: str) -> str:

    return {
        "DOMINO_OAUTH_TOKEN_URL": _TOKEN_URL,
        "DOMINO_OAUTH_CLIENT_ID": _CLIENT_ID,
        "DOMINO_OAUTH_CLIENT_SECRET": _CLIENT_SECRET,
        "DOMINO_OAUTH_SCOPE": _SCOPE,
        "DOMINO_OAUTH_AUDIENCE": _AUDIENCE
    }[parameter]


def _getenv_partial_side_effect(parameter: str) -> str:

    return {
        "DOMINO_OAUTH_TOKEN_URL": _TOKEN_URL,
        "DOMINO_OAUTH_CLIENT_ID": _CLIENT_ID,
        "DOMINO_OAUTH_CLIENT_SECRET": _CLIENT_SECRET
    }.get(parameter)


class OAuthAuthHandlerTest(TestCase):

    def setUp(self) -> None:
        self.oauth_authorization_client: OAuthAuthorizationClient = mock.create_autospec(OAuthAuthorizationClient)

    @mock.patch("os.getenv", side_effect=_getenv_side_effect)
    def test_should_create_session_context_successfully_execute(self, getenv_mock):

        # given
        oauth_config: OAuthConfig = OAuthConfig()
        oauth_auth_handler: OAuthAuthHandler = OAuthAuthHandler(oauth_config, self.oauth_authorization_client)
        self.oauth_authorization_client.request_authorization.return_value = self._prepare_client_response(True)

        # when
        result: SessionContext = oauth_auth_handler.create_session_context()

        # then
        self.assertEqual(result.username, _CLIENT_ID)
        self.assertEqual(result.authentication_token, _JWT_TOKEN)

        self.assertEqual(oauth_config.token_url, _TOKEN_URL)
        self.assertEqual(oauth_config.client_id, _CLIENT_ID)
        self.assertEqual(oauth_config.client_secret, _CLIENT_SECRET)
        self.assertEqual(oauth_config.scope, _SCOPE)
        self.assertEqual(oauth_config.audience, _AUDIENCE)

    def test_should_create_session_context_fail_for_missing_configuration(self):

        # given
        oauth_auth_handler: OAuthAuthHandler = OAuthAuthHandler(OAuthConfig(), self.oauth_authorization_client)

        # when
        with self.assertRaises(Exception) as exception_context:
            oauth_auth_handler.create_session_context()

        # then
        # exception expected
        self.assertEqual(str(exception_context.exception), "Insufficient configuration for OAuth authorization - please check the notes above")

    @mock.patch("os.getenv", side_effect=_getenv_partial_side_effect)
    def test_should_create_session_context_fail_for_partially_missing_configuration(self, getenv_mock):

        # given
        oauth_auth_handler: OAuthAuthHandler = OAuthAuthHandler(OAuthConfig(), self.oauth_authorization_client)

        # when
        with self.assertRaises(Exception) as exception_context:
            oauth_auth_handler.create_session_context()

        # then
        # exception expected
        self.assertEqual(str(exception_context.exception), "Insufficient configuration for OAuth authorization - please check the notes above")

    @mock.patch("os.getenv", side_effect=_getenv_side_effect)
    def test_should_create_session_context_fail_for_authorization_server_403_response(self, getenv_mock):

        # given
        oauth_auth_handler: OAuthAuthHandler = OAuthAuthHandler(OAuthConfig(), self.oauth_authorization_client)
        self.oauth_authorization_client.request_authorization.return_value = self._prepare_client_response(False)

        # when
        with self.assertRaises(Exception) as exception_context:
            oauth_auth_handler.create_session_context()

        # then
        # exception expected
        self.assertEqual(str(exception_context.exception), "Failed to authenticate - OAuth Authorization Server responded with 403")

    def test_should_for_auth_mode_return_oauth(self):

        # given
        oauth_auth_handler: OAuthAuthHandler = OAuthAuthHandler(OAuthConfig(), self.oauth_authorization_client)

        # when
        result: AuthMode = oauth_auth_handler.for_auth_mode()

        # then
        self.assertEqual(result, AuthMode.OAUTH)

    @staticmethod
    def _prepare_client_response(successful: bool):

        response: Response = mock.create_autospec(Response)
        if successful:
            response.status_code = 200
            response.json.return_value = {"access_token": _JWT_TOKEN}
        else:
            response.status_code = 403

        return response
