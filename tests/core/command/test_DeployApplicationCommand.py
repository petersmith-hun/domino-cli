import unittest
from unittest import mock

from domino_cli.core.command.DeployApplicationCommand import DeployApplicationCommand
from domino_cli.core.domain.CommandDescriptor import CommandDescriptor
from domino_cli.core.domain.DominoCommand import DominoCommand
from domino_cli.core.service.DominoService import DominoService
from tests.core.command.CommandBaseTest import CommandBaseTest


class DeployApplicationCommandTest(CommandBaseTest):

    def setUp(self) -> None:
        self.domino_service_mock: DominoService = mock.create_autospec(DominoService)

        self.deploy_application_command: DeployApplicationCommand = DeployApplicationCommand(self.domino_service_mock)

    def test_should_execute_command_for_latest_version(self):

        # given
        command_descriptor: CommandDescriptor = CommandDescriptor("deploy app1 latest")

        # when
        self.deploy_application_command.execute_command(command_descriptor)

        # then
        self.domino_service_mock.execute_lifecycle_command.assert_called_once_with(DominoCommand.DEPLOY_LATEST, "app1", "latest")

    def test_should_execute_command_for_specified_version(self):

        # given
        command_descriptor: CommandDescriptor = CommandDescriptor("deploy app1 1.0.0")

        # when
        self.deploy_application_command.execute_command(command_descriptor)

        # then
        self.domino_service_mock.execute_lifecycle_command.assert_called_once_with(DominoCommand.DEPLOY_VERSION, "app1", "1.0.0")

    @mock.patch("builtins.print", side_effect=print)
    def test_should_execute_command_fail_on_validation(self, print_mock):

        # given
        command_descriptor: CommandDescriptor = CommandDescriptor("deploy app1")

        # when
        self.deploy_application_command.execute_command(command_descriptor)

        # then
        self.assertEqual(self.domino_service_mock.call_count, 0)
        print_mock.assert_called_once_with("[error] Application name and 'latest' keyword or explicit version is required")

    def test_should_command_be_applicable_for_deploy_command(self):

        self.applicability_check(self.deploy_application_command, "deploy")


if __name__ == "__main__":
    unittest.main()
