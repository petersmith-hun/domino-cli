import unittest
from unittest import mock

from domino_cli.core.command.ImportCommand import ImportCommand
from domino_cli.core.domain.CommandDescriptor import CommandDescriptor
from domino_cli.core.service.DominoService import DominoService
from tests.core.command.CommandBaseTest import CommandBaseTest


class ImportCommandTest(CommandBaseTest):

    def setUp(self) -> None:
        self.domino_service_mock: DominoService = mock.create_autospec(DominoService)

        self.import_command: ImportCommand = ImportCommand(self.domino_service_mock)

    def test_should_execute_command_start_importing_definition_using_default_path(self):

        # given
        command_descriptor: CommandDescriptor = CommandDescriptor("import")

        # when
        self.import_command.execute_command(command_descriptor)

        # then
        self.domino_service_mock.import_definition.assert_called_once_with(None)

    def test_should_execute_command_start_importing_definition_using_defined_path(self):

        # given
        command_descriptor: CommandDescriptor = CommandDescriptor("import /opt/deployment.yml")

        # when
        self.import_command.execute_command(command_descriptor)

        # then
        self.domino_service_mock.import_definition.assert_called_once_with("/opt/deployment.yml")

    def test_should_execute_command_terminate_on_too_many_arguments(self):

        # given
        command_descriptor: CommandDescriptor = CommandDescriptor("import /opt/deployment.yml something")

        # when
        self.import_command.execute_command(command_descriptor)

        # then
        self.domino_service_mock.import_definition.assert_not_called()

    def test_should_command_be_applicable_for_help_command(self):

        self.applicability_check(self.import_command, "import")


if __name__ == "__main__":
    unittest.main()

