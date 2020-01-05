import unittest
from unittest import mock

import bcrypt
from requests import Response

from core.client.DominoClient import DominoClient
from core.domain.DominoRequest import DominoRequest
from core.domain.HTTPMethod import HTTPMethod
from core.domain.SessionContext import SessionContext
from core.service.AuthenticationService import AuthenticationService
from core.service.SessionContextHolder import SessionContextHolder

_JWT_TOKEN = "jwt_token"
_TEST_USERNAME = "test_user"
_TEST_PASSWORD = "test_pw"
_DOMINO_CLI_PASSWORD = "DOMINO_CLI_USERNAME"
_DOMINO_CLI_USERNAME = "DOMINO_CLI_USERNAME"


class AuthenticationServiceTest(unittest.TestCase):

    def setUp(self) -> None:
        self.domino_client_mock: DominoClient = mock.create_autospec(DominoClient)
        self.session_context_holder_mock: SessionContextHolder = mock.create_autospec(SessionContextHolder)

        self.authentication_service: AuthenticationService = AuthenticationService(self.domino_client_mock, self.session_context_holder_mock)

    @mock.patch("builtins.print", side_effect=print)
    @mock.patch("core.service.AuthenticationService.getpass", return_value=_TEST_PASSWORD)
    def test_should_encrypt_password_from_terminal(self, getpass_mock, print_mock):

        # given

        # when
        self.authentication_service.encrypt_password()

        # then
        self._assert_encrypted_password(print_mock)

    @mock.patch("builtins.print", side_effect=print)
    @mock.patch("os.getenv", return_value=_TEST_PASSWORD)
    def test_should_encrypt_password_from_env_variable(self, getenv_mock, print_mock):

        # when
        self.authentication_service.encrypt_password()

        # then
        self._assert_encrypted_password(print_mock)

    @mock.patch("builtins.print", side_effect=print)
    @mock.patch("os.getenv", side_effect=(lambda value: _TEST_USERNAME if value == _DOMINO_CLI_USERNAME else _TEST_PASSWORD))
    def test_should_generate_token_with_success_from_env_variable(self, getenv_mock, print_mock):

        # given
        self.domino_client_mock.send_command.return_value = AuthenticationServiceTest._prepare_client_response(True)

        # when
        self.authentication_service.generate_token()

        # then
        self.assertEqual(AuthenticationServiceTest._extract_print_value(print_mock), "Generated auth token: jwt_token")
        self._assert_domino_request()

    @mock.patch("builtins.print", side_effect=print)
    @mock.patch("builtins.input", return_value=_TEST_USERNAME)
    @mock.patch("core.service.AuthenticationService.getpass", return_value=_TEST_PASSWORD)
    def test_should_generate_token_with_success_from_terminal(self, getpass_mock, input_mock, print_mock):

        # given
        self.domino_client_mock.send_command.return_value = AuthenticationServiceTest._prepare_client_response(True)

        # when
        self.authentication_service.generate_token()

        # then
        self.assertEqual(AuthenticationServiceTest._extract_print_value(print_mock), "Generated auth token: jwt_token")
        self._assert_domino_request()

    @mock.patch("builtins.print", side_effect=print)
    @mock.patch("builtins.input", return_value=_TEST_USERNAME)
    @mock.patch("core.service.AuthenticationService.getpass", return_value=_TEST_PASSWORD)
    def test_should_generate_token_with_failure_from_terminal(self, getpass_mock, input_mock, print_mock):

        # given
        self.domino_client_mock.send_command.return_value = AuthenticationServiceTest._prepare_client_response(False)

        # when
        self.authentication_service.generate_token()

        # then
        self.assertEqual(AuthenticationServiceTest._extract_print_value(print_mock), "Failed to generate token - reason: Failed to authenticate - Domino responded with 403")
        self._assert_domino_request()

    @mock.patch("builtins.print", side_effect=print)
    @mock.patch("builtins.input", return_value=_TEST_USERNAME)
    @mock.patch("core.service.AuthenticationService.getpass", return_value=_TEST_PASSWORD)
    def test_should_open_session_with_success(self, getpass_mock, input_mock, print_mock):

        # given
        self.domino_client_mock.send_command.return_value = AuthenticationServiceTest._prepare_client_response(True)

        # when
        self.authentication_service.open_session()

        # then
        self.assertEqual(AuthenticationServiceTest._extract_print_value(print_mock), "Session is open")
        self._assert_domino_request()
        self.assertEqual(self.session_context_holder_mock.update.call_count, 1)
        session_context: SessionContext = self._extract_session_context()
        self.assertEqual(session_context.username, _TEST_USERNAME)
        self.assertEqual(session_context.authentication_token, _JWT_TOKEN)

    @mock.patch("builtins.print", side_effect=print)
    @mock.patch("builtins.input", return_value=_TEST_USERNAME)
    @mock.patch("core.service.AuthenticationService.getpass", return_value=_TEST_PASSWORD)
    def test_should_open_session_with_failure(self, getpass_mock, input_mock, print_mock):

        # given
        self.domino_client_mock.send_command.return_value = AuthenticationServiceTest._prepare_client_response(False)

        # when
        self.authentication_service.open_session()

        # then
        self.assertEqual(AuthenticationServiceTest._extract_print_value(print_mock), "Failed to open session - reason: Failed to authenticate - Domino responded with 403")
        self._assert_domino_request()
        self.assertEqual(self.session_context_holder_mock.call_count, 0)

    def _extract_session_context(self):
        return self.session_context_holder_mock.mock_calls[0][1][0]

    def _assert_encrypted_password(self, print_mock):
        encrypted_pw = AuthenticationServiceTest._extract_encrypted_password(print_mock)
        self.assertTrue(bcrypt.checkpw(_TEST_PASSWORD.encode("utf8"), encrypted_pw))

    @staticmethod
    def _extract_print_value(print_mock):
        return print_mock.mock_calls[0][1][0]

    @staticmethod
    def _extract_encrypted_password(print_mock):
        return str(AuthenticationServiceTest._extract_print_value(print_mock)) \
                .split(":")[1] \
                .strip() \
                .encode("utf8")

    @staticmethod
    def _prepare_client_response(successful: bool):

        response: Response = mock.create_autospec(Response)
        if successful:
            response.status_code = 201
            response.json.return_value = {"jwt": _JWT_TOKEN}
        else:
            response.status_code = 403

        return response

    def _assert_domino_request(self):
        domino_request: DominoRequest = self.domino_client_mock.send_command.mock_calls[0][1][0]
        self.assertEqual(domino_request.method, HTTPMethod.POST)
        self.assertEqual(domino_request.path, "/claim-token")
        self.assertEqual(domino_request.body, {"username": _TEST_USERNAME, "password": _TEST_PASSWORD})
        self.assertFalse(domino_request.authenticated)


if __name__ == "__main__":
    unittest.main()
