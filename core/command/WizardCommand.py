from core.command.AbstractCommand import AbstractCommand
from core.domain.CommandDescriptor import CommandDescriptor
from core.service.ConfigurationWizardService import ConfigurationWizardService


class WizardCommand(AbstractCommand):

    def __init__(self, configuration_wizard_service: ConfigurationWizardService):
        super().__init__("wizard")
        self._configuration_wizard_service: ConfigurationWizardService = configuration_wizard_service

    def execute_command(self, command_descriptor: CommandDescriptor) -> None:
        self._configuration_wizard_service.run_wizard()
