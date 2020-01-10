from core.command.AbstractCommand import AbstractCommand
from core.domain.CommandDescriptor import CommandDescriptor
from core.service.ConfigurationWizardService import ConfigurationWizardService

_COMMAND_NAME = "wizard"


class WizardCommand(AbstractCommand):

    def __init__(self, configuration_wizard_service: ConfigurationWizardService):
        super().__init__(_COMMAND_NAME)
        self._configuration_wizard_service: ConfigurationWizardService = configuration_wizard_service

    def execute_command(self, command_descriptor: CommandDescriptor) -> None:

        if not len(command_descriptor.arguments) == 1:
            print("Wizard name required")
            self._configuration_wizard_service.show_available_wizards()
        else:
            self._configuration_wizard_service.run_wizard(command_descriptor.arguments[0])
