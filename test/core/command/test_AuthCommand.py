import unittest
from unittest import mock

from core.command.AuthCommand import AuthCommand
from core.domain.CommandDescriptor import CommandDescriptor
from core.service.AuthenticationService import AuthenticationService
from test.core.command.CommandBaseTest import CommandBaseTest


class AuthCommandTest(CommandBaseTest):

    def setUp(self) -> None:
        self.authentication_service_mock: AuthenticationService = mock.create_autospec(AuthenticationService)

        self.auth_command: AuthCommand = AuthCommand(self.authentication_service_mock)

    def test_should_execute_command_for_encryption(self):

        # given
        command_descriptor: CommandDescriptor = CommandDescriptor("auth --encrypt-password")

        # when
        self.auth_command.execute_command(command_descriptor)

        # then
        self.assertEqual(len(self.authentication_service_mock.mock_calls), 1)
        self.assertEqual(self.authentication_service_mock.encrypt_password.call_count, 1)

    def test_should_execute_command_for_generating_token(self):

        # given
        command_descriptor: CommandDescriptor = CommandDescriptor("auth --generate-token")

        # when
        self.auth_command.execute_command(command_descriptor)

        # then
        self.assertEqual(len(self.authentication_service_mock.mock_calls), 1)
        self.assertEqual(self.authentication_service_mock.generate_token.call_count, 1)

    def test_should_execute_command_for_opening_session(self):

        # given
        command_descriptor: CommandDescriptor = CommandDescriptor("auth --open-session")

        # when
        self.auth_command.execute_command(command_descriptor)

        # then
        self.assertEqual(len(self.authentication_service_mock.mock_calls), 1)
        self.assertEqual(self.authentication_service_mock.open_session.call_count, 1)

    def test_should_execute_command_for_setting_mode_to_direct(self):

        # given
        command_descriptor: CommandDescriptor = CommandDescriptor("auth --set-mode direct")

        # when
        self.auth_command.execute_command(command_descriptor)

        # then
        self.assertEqual(len(self.authentication_service_mock.mock_calls), 1)
        self.assertEqual(self.authentication_service_mock.set_mode.call_count, 1)
        self.authentication_service_mock.set_mode.assert_called_with("direct")

    def test_should_execute_command_for_setting_mode_to_oauth(self):

        # given
        command_descriptor: CommandDescriptor = CommandDescriptor("auth --set-mode oauth")

        # when
        self.auth_command.execute_command(command_descriptor)

        # then
        self.assertEqual(len(self.authentication_service_mock.mock_calls), 1)
        self.assertEqual(self.authentication_service_mock.set_mode.call_count, 1)
        self.authentication_service_mock.set_mode.assert_called_with("oauth")

    def test_should_execute_command_for_setting_mode_without_mode_value(self):

        # given
        command_descriptor: CommandDescriptor = CommandDescriptor("auth --set-mode")

        # when
        self.auth_command.execute_command(command_descriptor)

        # then
        self.assertEqual(len(self.authentication_service_mock.mock_calls), 1)
        self.assertEqual(self.authentication_service_mock.set_mode.call_count, 1)
        self.authentication_service_mock.set_mode.assert_called_with(None)

    def test_should_execute_command_show_help_for_invalid_flag(self):

        # given
        command_descriptor: CommandDescriptor = CommandDescriptor("auth --non-existing-flag")

        # when
        self.auth_command.execute_command(command_descriptor)

        # then
        self.assertEqual(len(self.authentication_service_mock.mock_calls), 0)

    def test_should_execute_command_show_help_for_missing_flag(self):

        # given
        command_descriptor: CommandDescriptor = CommandDescriptor("auth")

        # when
        self.auth_command.execute_command(command_descriptor)

        # then
        self.assertEqual(len(self.authentication_service_mock.mock_calls), 0)

    def test_should_command_be_applicable_for_auth_command(self):

        self.applicability_check(self.auth_command, "auth")


if __name__ == "__main__":
    unittest.main()
