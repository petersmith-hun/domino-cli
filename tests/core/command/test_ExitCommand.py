import unittest
from unittest import mock

from domino_cli.core.command.ExitCommand import ExitCommand
from domino_cli.core.domain.CommandDescriptor import CommandDescriptor
from tests.core.command.CommandBaseTest import CommandBaseTest


class ExitCommandTest(CommandBaseTest):

    def setUp(self) -> None:
        self.exit_command: ExitCommand = ExitCommand()

    @mock.patch("builtins.print", side_effect=print)
    def test_should_execute_command_say_goodbye(self, print_mock):

        # given
        command_descriptor: CommandDescriptor = CommandDescriptor("exit")

        # when
        self.exit_command.execute_command(command_descriptor)

        # then
        print_mock.assert_called_once_with("[info ] Bye!")

    def test_should_command_be_applicable_for_exit_command(self):

        self.applicability_check(self.exit_command, "exit")


if __name__ == "__main__":
    unittest.main()
