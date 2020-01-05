import unittest
from unittest import mock

from core.cli.CLI import CLI
from core.domain.CommandDescriptor import CommandDescriptor
from core.service.CommandProcessor import CommandProcessor

_COMMANDS = ["cmd1", "cmd2", "exit"]


class CLITest(unittest.TestCase):

    def setUp(self) -> None:
        self.command_processor_mock: CommandProcessor = mock.create_autospec(CommandProcessor)
        self.cli: CLI = CLI(self.command_processor_mock)

    @mock.patch("builtins.input", side_effect=_COMMANDS)
    def test_should_run_loop_until_exit_command(self, input_mock) -> None:

        # given
        processor_responses = [True, True, False]
        self.command_processor_mock.execute_command.side_effect = processor_responses

        # when
        self.cli.run_loop()

        # then
        self.assertEqual(self.command_processor_mock.execute_command.call_count, 3)
        for (name, args, kwargs) in self.command_processor_mock.execute_command.mock_calls:
            call_parameter = args[0]
            self.assertIsInstance(call_parameter, CommandDescriptor)
            self.assertIn(call_parameter.command, _COMMANDS)


if __name__ == "__main__":
    unittest.main()
