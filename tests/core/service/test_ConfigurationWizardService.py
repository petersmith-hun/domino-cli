import unittest
from unittest import mock

from domino_cli.core.service.ConfigurationWizardService import ConfigurationWizardService
from domino_cli.core.service.wizard.AbstractWizard import AbstractWizard

_AVAILABLE_WIZARDS_EXPECTED_HELP = "Available wizards:\n[           wiz1]: wiz1_desc\n[           wiz2]: wiz2_desc"


class ConfigurationWizardServiceTest(unittest.TestCase):

    def setUp(self) -> None:
        self.abstract_wizard_1: AbstractWizard = mock.create_autospec(AbstractWizard)
        self.abstract_wizard_2: AbstractWizard = mock.create_autospec(AbstractWizard)

        self.abstract_wizard_1.get_wizard_name.return_value = "wiz1"
        self.abstract_wizard_1.get_wizard_description.return_value = "wiz1_desc"
        self.abstract_wizard_2.get_wizard_name.return_value = "wiz2"
        self.abstract_wizard_2.get_wizard_description.return_value = "wiz2_desc"

        self.configuration_wizard_service: ConfigurationWizardService = ConfigurationWizardService([
            self.abstract_wizard_1,
            self.abstract_wizard_2])

    @mock.patch("builtins.print", side_effect=print)
    def test_should_show_available_wizards_list_registered_wizards(self, print_mock):

        # when
        self.configuration_wizard_service.show_available_wizards()

        # then
        print_mock.assert_called_once_with(_AVAILABLE_WIZARDS_EXPECTED_HELP)

    def test_should_run_wizard_execute_existing_wizard(self):

        # when
        self.configuration_wizard_service.run_wizard("wiz2")

        # then
        self.assertEqual(self.abstract_wizard_2.run.call_count, 1)

    @mock.patch("builtins.print", side_effect=print)
    def test_should_run_wizard_show_help_for_non_existing_wizard(self, print_mock):

        # when
        self.configuration_wizard_service.run_wizard("non-existing-wizard")

        # then
        print_mock.assert_has_calls([
            mock.call("Unknown wizard 'non-existing-wizard'"),
            mock.call(_AVAILABLE_WIZARDS_EXPECTED_HELP)
        ])
        self.assertEqual(self.abstract_wizard_1.run.call_count, 0)
        self.assertEqual(self.abstract_wizard_2.run.call_count, 0)


if __name__ == "__main__":
    unittest.main()
