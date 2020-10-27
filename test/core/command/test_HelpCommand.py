import unittest
from unittest import mock

from core.command.HelpCommand import HelpCommand
from core.domain.CommandDescriptor import CommandDescriptor
from test.core.command.CommandBaseTest import CommandBaseTest


class HelpCommandTest(CommandBaseTest):

    def setUp(self) -> None:
        self.help_command: HelpCommand = HelpCommand()

    @mock.patch("builtins.print", side_effect=print)
    def test_should_execute_command_show_help_text(self, print_mock):

        # given
        command_descriptor: CommandDescriptor = CommandDescriptor("help")

        # when
        self.help_command.execute_command(command_descriptor)

        # then
        self.assertGreaterEqual(print_mock.call_count, 3)

    def test_should_command_be_applicable_for_help_command(self):

        self.applicability_check(self.help_command, "help")


if __name__ == "__main__":
    unittest.main()
