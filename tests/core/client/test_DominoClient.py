import unittest
from unittest import mock

from domino_cli.core.client.DominoClient import DominoClient
from domino_cli.core.domain.DominoRequest import DominoRequest
from domino_cli.core.domain.HTTPMethod import HTTPMethod
from domino_cli.core.domain.SessionContext import SessionContext
from domino_cli.core.service.SessionContextHolder import SessionContextHolder

_HTTP_METHOD = HTTPMethod.GET
_PATH = "/lifecycle"
_DOMINO_BASE_URL: str = "http://localhost:8080"
_RESOLVED_PATH = _DOMINO_BASE_URL + _PATH
_AUTH_HEADER = {"Authorization": "Bearer token"}
_BODY = {"message": "value"}
_SESSION_CONTEXT: SessionContext = SessionContext("username", "token")


class DominoClientTest(unittest.TestCase):

    def setUp(self) -> None:
        self.session_context_holder: SessionContextHolder = mock.create_autospec(SessionContextHolder)
        self.domino_client: DominoClient = DominoClient(_DOMINO_BASE_URL, self.session_context_holder)

    @mock.patch("requests.request")
    def test_should_send_command_execute_http_request_with_authentication_and_body(self, request_mock) -> None:

        # given
        self.session_context_holder.get_bearer_auth.return_value = _AUTH_HEADER
        domino_request: DominoRequest = DominoRequest(_HTTP_METHOD, _PATH, body=_BODY, authenticated=True)

        # when
        self.domino_client.send_command(domino_request)

        # then
        request_mock.assert_called_once_with(_HTTP_METHOD.value, _RESOLVED_PATH, json=_BODY, headers=_AUTH_HEADER)

    @mock.patch("requests.request")
    def test_should_send_command_execute_http_request_without_authentication_and_body(self, request_mock) -> None:

        # given
        domino_request: DominoRequest = DominoRequest(_HTTP_METHOD, _PATH, authenticated=False)

        # when
        self.domino_client.send_command(domino_request)

        # then
        request_mock.assert_called_once_with(_HTTP_METHOD.value, _RESOLVED_PATH, json=None, headers=None)
        self.assertEqual(self.session_context_holder.get_bearer_auth.call_count, 0)

    @mock.patch("requests.request")
    def test_should_send_command_execute_http_request_with_non_initialized_session(self, request_mock) -> None:

        # given
        self.session_context_holder.get_bearer_auth.return_value = None
        domino_request: DominoRequest = DominoRequest(_HTTP_METHOD, _PATH, authenticated=True)

        # when
        self.domino_client.send_command(domino_request)

        # then
        request_mock.assert_called_once_with(_HTTP_METHOD.value, _RESOLVED_PATH, json=None, headers=None)


if __name__ == "__main__":
    unittest.main()
