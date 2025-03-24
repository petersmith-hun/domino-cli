import unittest
from unittest import mock

from domino_cli.core.command.InfoCommand import InfoCommand
from domino_cli.core.domain.CommandDescriptor import CommandDescriptor
from domino_cli.core.domain.DominoCommand import DominoCommand
from domino_cli.core.service.DominoService import DominoService
from tests.core.command.CommandBaseTest import CommandBaseTest


class InfoCommandTest(CommandBaseTest):

    def setUp(self) -> None:
        self.domino_service_mock: DominoService = mock.create_autospec(DominoService)

        self.info_command: InfoCommand = InfoCommand(self.domino_service_mock)

    def test_should_execute_command_with_success(self):

        # given
        command_descriptor: CommandDescriptor = CommandDescriptor("info app1")

        # when
        self.info_command.execute_command(command_descriptor)

        # then
        self.domino_service_mock.execute_lifecycle_command.assert_called_once_with(DominoCommand.INFO, "app1")

    @mock.patch("builtins.print", side_effect=print)
    def test_should_execute_command_fail_on_validation(self, print_mock):

        # given
        command_descriptor: CommandDescriptor = CommandDescriptor("info")

        # when
        self.info_command.execute_command(command_descriptor)

        # then
        self.assertEqual(self.domino_service_mock.call_count, 0)
        print_mock.assert_called_once_with("[warn ] Application name required")

    def test_should_command_be_applicable_for_info_command(self):

        self.applicability_check(self.info_command, "info")


if __name__ == "__main__":
    unittest.main()
