import unittest
from unittest import mock

from domino_cli.core.command.AbstractCommand import AbstractCommand
from domino_cli.core.command.ExitCommand import ExitCommand
from domino_cli.core.domain.CommandDescriptor import CommandDescriptor
from domino_cli.core.service.CommandProcessor import CommandProcessor


class CommandProcessorTest(unittest.TestCase):

    def setUp(self) -> None:
        self.command_exit_mock: ExitCommand = mock.create_autospec(ExitCommand)
        self.command_default_mock: AbstractCommand = mock.create_autospec(AbstractCommand, _name="default_cmd")
        self.command_cmd1_mock: AbstractCommand = mock.create_autospec(AbstractCommand, _name="cmd1")
        self.command_cmd2_mock: AbstractCommand = mock.create_autospec(AbstractCommand, _name="cmd2")

        self.command_exit_mock.is_applicable.return_value = False
        self.command_default_mock.is_applicable.return_value = False
        self.command_cmd1_mock.is_applicable.return_value = False
        self.command_cmd2_mock.is_applicable.return_value = False

        self.command_processor: CommandProcessor = CommandProcessor(self.command_default_mock, [
            self.command_default_mock,
            self.command_cmd1_mock,
            self.command_cmd2_mock,
            self.command_exit_mock])

    def test_should_execute_applicable_command(self) -> None:

        # given
        command_descriptor: CommandDescriptor = CommandDescriptor("cmd2")
        self.command_cmd2_mock.is_applicable.return_value = True

        # when
        result: bool = self.command_processor.execute_command(command_descriptor)

        # then
        self.assertTrue(result)
        self.assertTrue(self.command_cmd2_mock.execute_command.called)

    def test_should_execute_default_command(self) -> None:

        # given
        command_descriptor: CommandDescriptor = CommandDescriptor("unknown")

        # when
        result: bool = self.command_processor.execute_command(command_descriptor)

        # then
        self.assertTrue(result)
        self.assertTrue(self.command_default_mock.execute_command.called)

    def test_should_execute_exit_command(self) -> None:

        # given
        command_descriptor: CommandDescriptor = CommandDescriptor("exit")
        self.command_exit_mock.is_applicable.return_value = True

        # when
        result: bool = self.command_processor.execute_command(command_descriptor)

        # then
        self.assertFalse(result)
        self.assertTrue(self.command_exit_mock.execute_command.called)


if __name__ == "__main__":
    unittest.main()
