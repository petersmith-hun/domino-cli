from unittest import TestCase, mock

from requests import Response

from domino_cli.core.client.DominoClient import DominoClient
from domino_cli.core.domain.AuthMode import AuthMode
from domino_cli.core.domain.DominoRequest import DominoRequest
from domino_cli.core.domain.HTTPMethod import HTTPMethod
from domino_cli.core.domain.SessionContext import SessionContext
from domino_cli.core.service.auth.DirectAuthHandler import DirectAuthHandler

_JWT_TOKEN = "jwt_token"
_TEST_USERNAME_CONSOLE = "test_user_console"
_TEST_PASSWORD_CONSOLE = "test_pw_console"
_TEST_USERNAME_ENV = "test_user_env"
_TEST_PASSWORD_ENV = "test_pw_env"
_DOMINO_CLI_USERNAME = "DOMINO_CLI_USERNAME"


class DirectAuthHandlerTest(TestCase):

    def setUp(self) -> None:
        self.domino_client_mock: DominoClient = mock.create_autospec(DominoClient)

        self.direct_auth_handler: DirectAuthHandler = DirectAuthHandler(self.domino_client_mock)

    @mock.patch("builtins.input", return_value=_TEST_USERNAME_CONSOLE)
    @mock.patch("domino_cli.core.service.auth.AuthUtils.getpass", return_value=_TEST_PASSWORD_CONSOLE)
    def test_should_create_session_context_successfully_execute_with_credentials_from_console(self, getpass_mock, input_mock):

        # given
        self.domino_client_mock.send_command.return_value = self._prepare_client_response(True)

        # when
        result: SessionContext = self.direct_auth_handler.create_session_context()

        # then
        self.assertEqual(result.username, _TEST_USERNAME_CONSOLE)
        self.assertEqual(result.authentication_token, _JWT_TOKEN)
        self._assert_domino_request(_TEST_USERNAME_CONSOLE, _TEST_PASSWORD_CONSOLE)

    @mock.patch("os.getenv", side_effect=(lambda value: _TEST_USERNAME_ENV if value == _DOMINO_CLI_USERNAME else _TEST_PASSWORD_ENV))
    def test_should_create_session_context_successfully_execute_with_credentials_from_environment(self, getenv_mock):

        # given
        self.domino_client_mock.send_command.return_value = self._prepare_client_response(True)

        # when
        result: SessionContext = self.direct_auth_handler.create_session_context()

        # then
        self.assertEqual(result.username, _TEST_USERNAME_ENV)
        self.assertEqual(result.authentication_token, _JWT_TOKEN)
        self._assert_domino_request(_TEST_USERNAME_ENV, _TEST_PASSWORD_ENV)

    @mock.patch("os.getenv", side_effect=(lambda value: _TEST_USERNAME_ENV if value == _DOMINO_CLI_USERNAME else _TEST_PASSWORD_ENV))
    def test_should_create_session_context_fail_on_domino_403_response(self, getenv_mock):

        # given
        self.domino_client_mock.send_command.return_value = self._prepare_client_response(False)

        # when
        with self.assertRaises(Exception, ) as exception_context:
            self.direct_auth_handler.create_session_context()

        # then
        # exception expected
        self._assert_domino_request(_TEST_USERNAME_ENV, _TEST_PASSWORD_ENV)
        self.assertEqual(str(exception_context.exception), "Failed to authenticate - Domino responded with 403")

    def test_should_for_auth_mode_return_direct(self):

        # when
        result: AuthMode = self.direct_auth_handler.for_auth_mode()

        # then
        self.assertEqual(result, AuthMode.DIRECT)

    @staticmethod
    def _prepare_client_response(successful: bool):

        response: Response = mock.create_autospec(Response)
        if successful:
            response.status_code = 201
            response.json.return_value = {"jwt": _JWT_TOKEN}
        else:
            response.status_code = 403

        return response

    def _assert_domino_request(self, expected_username: str, expected_password: str):
        domino_request: DominoRequest = self.domino_client_mock.send_command.call_args.args[0]
        self.assertEqual(domino_request.method, HTTPMethod.POST)
        self.assertEqual(domino_request.path, "/claim-token")
        self.assertEqual(domino_request.body, {"username": expected_username, "password": expected_password})
        self.assertFalse(domino_request.authenticated)
