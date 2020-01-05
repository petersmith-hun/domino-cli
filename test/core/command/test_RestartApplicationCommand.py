import unittest
from unittest import mock

from core.command.RestartApplicationCommand import RestartApplicationCommand
from core.domain.CommandDescriptor import CommandDescriptor
from core.domain.DominoCommand import DominoCommand
from core.service.DominoService import DominoService
from test.core.command.CommandBaseTest import CommandBaseTest


class RestartApplicationCommandTest(CommandBaseTest):

    def setUp(self) -> None:
        self.domino_service_mock: DominoService = mock.create_autospec(DominoService)

        self.restart_application_command: RestartApplicationCommand = RestartApplicationCommand(self.domino_service_mock)

    def test_should_execute_command_with_success(self):

        # given
        command_descriptor: CommandDescriptor = CommandDescriptor("restart app1")

        # when
        self.restart_application_command.execute_command(command_descriptor)

        # then
        self.domino_service_mock.execute_lifecycle_command.assert_called_once_with(DominoCommand.RESTART, "app1")

    @mock.patch("builtins.print", side_effect=print)
    def test_should_execute_command_fail_on_validation(self, print_mock):

        # given
        command_descriptor: CommandDescriptor = CommandDescriptor("restart")

        # when
        self.restart_application_command.execute_command(command_descriptor)

        # then
        self.assertEqual(self.domino_service_mock.call_count, 0)
        print_mock.assert_called_once_with("Application name required")

    def test_should_command_be_applicable_for_restart_command(self):

        self.applicability_check(self.restart_application_command, "restart")


if __name__ == "__main__":
    unittest.main()
