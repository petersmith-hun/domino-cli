import unittest

from domino_cli.core.command.AbstractCommand import AbstractCommand
from domino_cli.core.domain.CommandDescriptor import CommandDescriptor


_COMMAND_LIST = ["start", "stop", "restart", "deploy", "help", "exit", "auth", "wizard", "info", "import"]


class CommandBaseTest(unittest.TestCase):

    def applicability_check(self, command_under_test: AbstractCommand, applicable_for: str):

        # given
        for (command, expected_applicability) in CommandBaseTest._prepare_parameters(applicable_for):
            with self.subTest("test_applicability", command=command, expected_applicability=expected_applicability):

                # when
                result: bool = command_under_test.is_applicable(CommandDescriptor(command))

                # then
                self.assertEqual(result, expected_applicability)

    @staticmethod
    def _prepare_parameters(applicable_for: str):
        return [(command, command == applicable_for) for command in _COMMAND_LIST]
