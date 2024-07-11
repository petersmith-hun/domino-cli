from domino_cli.core.command.AbstractCommand import AbstractCommand
from domino_cli.core.domain.CommandDescriptor import CommandDescriptor
from domino_cli.core.service.ConfigurationWizardService import ConfigurationWizardService

_COMMAND_NAME = "wizard"


class WizardCommand(AbstractCommand):
    """
    Command implementation for wizard related operations.
    """
    def __init__(self, configuration_wizard_service: ConfigurationWizardService):
        super().__init__(_COMMAND_NAME)
        self._configuration_wizard_service: ConfigurationWizardService = configuration_wizard_service

    def execute_command(self, command_descriptor: CommandDescriptor) -> None:
        """
        Instructs ConfigurationWizardService to start execution of the specified wizard.
        Shows available wizards in case of missing wizard name parameter.

        :param command_descriptor: CommandDescriptor object containing the command arguments
        """
        if not len(command_descriptor.arguments) == 1:
            print("Wizard name required")
            self._configuration_wizard_service.show_available_wizards()
        else:
            self._configuration_wizard_service.run_wizard(command_descriptor.arguments[0])
