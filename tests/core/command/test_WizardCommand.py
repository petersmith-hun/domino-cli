import unittest
from unittest import mock

from domino_cli.core.command.WizardCommand import WizardCommand
from domino_cli.core.domain.CommandDescriptor import CommandDescriptor
from domino_cli.core.service.ConfigurationWizardService import ConfigurationWizardService
from tests.core.command.CommandBaseTest import CommandBaseTest


class WizardCommandTest(CommandBaseTest):

    def setUp(self) -> None:
        self.configuration_wizard_service_mock: ConfigurationWizardService = mock.create_autospec(ConfigurationWizardService)

        self.wizard_command: WizardCommand = WizardCommand(self.configuration_wizard_service_mock)

    def test_should_execute_command_to_start_wizard(self):

        # given
        command_descriptor: CommandDescriptor = CommandDescriptor("wizard wiz1")

        # when
        self.wizard_command.execute_command(command_descriptor)

        # then
        self.configuration_wizard_service_mock.run_wizard.assert_called_once_with("wiz1")

    @mock.patch("builtins.print", side_effect=print)
    def test_should_execute_command_fail_on_validation(self, print_mock):

        # given
        command_descriptor: CommandDescriptor = CommandDescriptor("wizard")

        # when
        self.wizard_command.execute_command(command_descriptor)

        # then
        print_mock.assert_called_once_with("Wizard name required")
        self.assertEqual(self.configuration_wizard_service_mock.show_available_wizards.call_count, 1)
        self.assertEqual(self.configuration_wizard_service_mock.run_wizard.call_count, 0)

    def test_should_command_be_applicable_for_wizard_command(self):

        self.applicability_check(self.wizard_command, "wizard")


if __name__ == "__main__":
    unittest.main()
