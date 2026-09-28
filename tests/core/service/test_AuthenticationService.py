import datetime
import unittest
from unittest import mock

import bcrypt

from domino_cli import RuntimeHelper
from domino_cli.core.domain.AuthMode import AuthMode
from domino_cli.core.domain.CustomExceptions import AuthenticationException
from domino_cli.core.domain.SessionContext import SessionContext
from domino_cli.core.service.AuthenticationService import AuthenticationService
from domino_cli.core.service.SessionContextHolder import SessionContextHolder
from domino_cli.core.service.auth.AbstractAuthHandler import AbstractAuthHandler

_JWT_TOKEN = "jwt_token"
_TEST_USERNAME = "test_user"
_TEST_PASSWORD = "test_pw"
_DOMINO_CLI_PASSWORD = "DOMINO_CLI_USERNAME"
_DOMINO_CLI_USERNAME = "DOMINO_CLI_USERNAME"
_MOCK_SESSION_CONTEXT = SessionContext(_TEST_USERNAME, _JWT_TOKEN, datetime.datetime.now())


class AuthenticationServiceTest(unittest.TestCase):

    def setUp(self) -> None:
        self.direct_auth_handler_mock: AbstractAuthHandler = mock.create_autospec(AbstractAuthHandler)
        self.oauth_auth_handler_mock: AbstractAuthHandler = mock.create_autospec(AbstractAuthHandler)
        self.session_context_holder_mock: SessionContextHolder = mock.create_autospec(SessionContextHolder)

        self.direct_auth_handler_mock.for_auth_mode.return_value = AuthMode.DIRECT
        self.oauth_auth_handler_mock.for_auth_mode.return_value = AuthMode.OAUTH

        self.authentication_service: AuthenticationService = \
            AuthenticationService(AuthMode.DIRECT, self.session_context_holder_mock,
                                  [self.direct_auth_handler_mock, self.oauth_auth_handler_mock])

    @mock.patch("domino_cli.core.service.auth.AuthUtils.getpass", return_value=_TEST_PASSWORD)
    def test_should_encrypt_password_from_terminal(self, getpass_mock):

        # given
        RuntimeHelper._cli_mode = True

        # when
        result = self.authentication_service.encrypt_password()

        # then
        self._assert_encrypted_password(result)

    @mock.patch("os.getenv", return_value=_TEST_PASSWORD)
    def test_should_encrypt_password_from_env_variable(self, getenv_mock):

        # when
        result = self.authentication_service.encrypt_password()

        # then
        self._assert_encrypted_password(result)

    @mock.patch("os.getenv", side_effect=(lambda value: _TEST_USERNAME if value == _DOMINO_CLI_USERNAME else _TEST_PASSWORD))
    def test_should_generate_token_with_success_from_env_variable(self, getenv_mock):

        # given
        self.direct_auth_handler_mock.create_session_context.return_value = _MOCK_SESSION_CONTEXT

        # when
        result = self.authentication_service.generate_token()

        # then
        self.assertEqual(result, "jwt_token")

    @mock.patch("builtins.input", return_value=_TEST_USERNAME)
    @mock.patch("domino_cli.core.service.auth.AuthUtils.getpass", return_value=_TEST_PASSWORD)
    def test_should_generate_token_with_failure_from_terminal(self, getpass_mock, input_mock):

        # given
        self.direct_auth_handler_mock.create_session_context.side_effect = Exception("Failed to authenticate")

        # when
        throwing = lambda: self.authentication_service.generate_token()

        # then
        self.assertRaises(AuthenticationException, throwing)

    @mock.patch("builtins.input", return_value=_TEST_USERNAME)
    @mock.patch("builtins.input", return_value=_TEST_USERNAME)
    @mock.patch("domino_cli.core.service.auth.AuthUtils.getpass", return_value=_TEST_PASSWORD)
    def test_should_open_session_with_success(self, getpass_mock, input_mock, input_mock_2):

        # given
        self.direct_auth_handler_mock.create_session_context.return_value = _MOCK_SESSION_CONTEXT

        # when
        result = self.authentication_service.open_session()

        # then
        self.assertEqual(self.session_context_holder_mock.update.call_count, 1)
        session_context: SessionContext = self._extract_session_context()
        self.assertEqual(session_context.username, _TEST_USERNAME)
        self.assertEqual(session_context.authentication_token, _JWT_TOKEN)

    @mock.patch("builtins.input", return_value=_TEST_USERNAME)
    @mock.patch("domino_cli.core.service.auth.AuthUtils.getpass", return_value=_TEST_PASSWORD)
    def test_should_open_session_with_failure(self, getpass_mock, input_mock):

        # given
        self.direct_auth_handler_mock.create_session_context.side_effect = Exception("Failed to authenticate")

        # when
        throwing = lambda: self.authentication_service.open_session()

        # then
        self.assertRaises(AuthenticationException, throwing)
        self.assertEqual(self.session_context_holder_mock.call_count, 0)

    def test_should_set_mode_to_direct(self):

        # when
        self.authentication_service.set_mode("direct")

        # then
        self.assertEqual(self.authentication_service._auth_mode, AuthMode.DIRECT)

    def test_should_set_mode_to_oauth(self):

        # when
        self.authentication_service.set_mode("oauth")

        # then
        self.assertEqual(self.authentication_service._auth_mode, AuthMode.OAUTH)

    @mock.patch("builtins.print", side_effect=print)
    def test_should_set_mode_fail_on_invalid_value(self, print_mock):

        # when
        self.authentication_service.set_mode("invalid")

        # then
        self.assertEqual(self.authentication_service._auth_mode, AuthMode.DIRECT)
        self.assertEqual(AuthenticationServiceTest._extract_print_value(print_mock), "[error] Failed to change authentication mode, invalid mode defined: invalid")

    def _extract_session_context(self):
        return self.session_context_holder_mock.mock_calls[0][1][0]

    def _assert_encrypted_password(self, encrypted_password: str):
        self.assertTrue(bcrypt.checkpw(_TEST_PASSWORD.encode("utf8"), encrypted_password.encode("utf8")))

    @staticmethod
    def _extract_print_value(print_mock):
        return print_mock.call_args.args[0]


if __name__ == "__main__":
    unittest.main()
