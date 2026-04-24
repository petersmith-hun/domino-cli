import unittest
from unittest import mock

from domino_cli.core.command.OAuthImportCommand import OAuthImportCommand
from domino_cli.core.domain.CommandDescriptor import CommandDescriptor
from domino_cli.core.service.DominoService import DominoService
from tests.core.command.CommandBaseTest import CommandBaseTest


class OAuthImportCommandTest(CommandBaseTest):

    def setUp(self) -> None:
        self.domino_service_mock: DominoService = mock.create_autospec(DominoService)

        self.oauth_import_command: OAuthImportCommand = OAuthImportCommand(self.domino_service_mock)

    def test_should_execute_command_start_importing_oauth_descriptor_using_default_path(self):

        # given
        command_descriptor: CommandDescriptor = CommandDescriptor("oauth-import app")

        # when
        self.oauth_import_command.execute_command(command_descriptor)

        # then
        self.domino_service_mock.import_oauth_descriptor.assert_called_once_with("app", False, None)

    def test_should_execute_command_start_importing_oauth_descriptor_using_default_path_in_dry_run(self):

        # given
        command_descriptor: CommandDescriptor = CommandDescriptor("oauth-import app --dry-run")

        # when
        self.oauth_import_command.execute_command(command_descriptor)

        # then
        self.domino_service_mock.import_oauth_descriptor.assert_called_once_with("app", True, None)

    def test_should_execute_command_start_importing_oauth_descriptor_using_defined_path(self):

        # given
        command_descriptor: CommandDescriptor = CommandDescriptor("oauth-import app /opt/deployment.yml")

        # when
        self.oauth_import_command.execute_command(command_descriptor)

        # then
        self.domino_service_mock.import_oauth_descriptor.assert_called_once_with("app", False, "/opt/deployment.yml")

    def test_should_execute_command_start_importing_oauth_descriptor_using_defined_path_in_dry_run(self):

        # given
        command_descriptor: CommandDescriptor = CommandDescriptor("oauth-import app --dry-run /opt/deployment.yml")

        # when
        self.oauth_import_command.execute_command(command_descriptor)

        # then
        self.domino_service_mock.import_oauth_descriptor.assert_called_once_with("app", True, "/opt/deployment.yml")

    def test_should_execute_command_terminate_on_too_many_arguments(self):

        # given
        command_descriptor: CommandDescriptor = CommandDescriptor("oauth-import /opt/deployment.yml something something else")

        # when
        self.oauth_import_command.execute_command(command_descriptor)

        # then
        self.domino_service_mock.import_oauth_descriptor.assert_not_called()

    def test_should_execute_command_terminate_on_too_few_arguments(self):

        # given
        command_descriptor: CommandDescriptor = CommandDescriptor("oauth-import")

        # when
        self.oauth_import_command.execute_command(command_descriptor)

        # then
        self.domino_service_mock.import_oauth_descriptor.assert_not_called()

    def test_should_command_be_applicable_for_help_command(self):

        self.applicability_check(self.oauth_import_command, "oauth-import")


if __name__ == "__main__":
    unittest.main()
