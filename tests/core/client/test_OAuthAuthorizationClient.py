import base64
from unittest import TestCase, mock

from domino_cli.core.client.OAuthAuthorizationClient import OAuthAuthorizationClient
from domino_cli.core.domain.OAuthConfig import OAuthConfig

_TOKEN_URL = "http://localhost:9999/token"
_CLIENT_ID = "domino-cli-1"
_CLIENT_SECRET = "domino1234"
_SCOPE = "read:info"
_AUDIENCE = "aud:domino"


class OAuthAuthorizationClientTest(TestCase):

    @mock.patch("requests.request")
    def test_should_request_authorization_execute_with_audience(self, request_mock):

        # given
        oauth_config: OAuthConfig = self._prepare_oauth_config(True)
        oauth_authorization_client: OAuthAuthorizationClient = OAuthAuthorizationClient(oauth_config)

        # when
        oauth_authorization_client.request_authorization()

        # then
        self._verify_request(True, request_mock.call_args.args[0], request_mock.call_args.args[1],
                             request_mock.call_args.kwargs["data"], request_mock.call_args.kwargs["headers"])

    @mock.patch("requests.request")
    def test_should_request_authorization_execute_without_audience(self, request_mock):

        # given
        oauth_config: OAuthConfig = self._prepare_oauth_config(False)
        oauth_authorization_client: OAuthAuthorizationClient = OAuthAuthorizationClient(oauth_config)

        # when
        oauth_authorization_client.request_authorization()

        # then
        self._verify_request(False, request_mock.call_args.args[0], request_mock.call_args.args[1],
                             request_mock.call_args.kwargs["data"], request_mock.call_args.kwargs["headers"])

    def _verify_request(self, with_audience: bool, method: str, url: str, data: dict, headers: dict) -> None:

        self.assertEqual(method, "POST")

        if with_audience:
            self.assertEqual(url, f"{_TOKEN_URL}?audience={_AUDIENCE}")
        else:
            self.assertEqual(url, _TOKEN_URL)

        self.assertEqual(data, {
            "grant_type": "client_credentials",
            "client_id": _CLIENT_ID,
            "scope": _SCOPE
        })

        self.assertEqual(len(headers), 1)

        authorization: str = headers.get("Authorization")
        self.assertIsNotNone(authorization)
        self.assertTrue(authorization.startswith("Basic "))

        encoded_credentials: str = authorization[6:]
        decoded_credentials: str = base64.b64decode(encoded_credentials).decode("UTF-8")
        self.assertEqual(decoded_credentials, f"{_CLIENT_ID}:{_CLIENT_SECRET}")

    @staticmethod
    def _prepare_oauth_config(with_audience: bool) -> OAuthConfig:

        oauth_config: OAuthConfig = OAuthConfig()
        oauth_config.token_url = _TOKEN_URL
        oauth_config.client_id = _CLIENT_ID
        oauth_config.client_secret = _CLIENT_SECRET
        oauth_config.scope = _SCOPE

        if with_audience:
            oauth_config.audience = _AUDIENCE

        return oauth_config
