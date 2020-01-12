from typing import List, Dict

from core.service.wizard.AbstractWizard import AbstractWizard

_WIZARD_HELP_TEXT_LINE = "{}\n[{:>15}]: {}"


class ConfigurationWizardService:
    """
    Service implementation managing configuration wizard tasks.
    """
    def __init__(self, wizards: List[AbstractWizard]):
        self._wizards: Dict[str, AbstractWizard] = {wizard.get_wizard_name(): wizard for wizard in wizards}
        self._available_wizards_help: str = self._prepare_available_wizards_help()

    def show_available_wizards(self) -> None:
        """
        Prints the name and the description of the available wizards.
        """
        print("Available wizards:{0}".format(self._available_wizards_help))

    def run_wizard(self, wizard_name: str) -> None:
        """
        Executes the selected wizard if it exists (otherwise prints the available wizards).

        :param wizard_name: name of the wizard to be executed
        """
        if wizard_name not in self._wizards.keys():
            print("Unknown wizard '{0}'".format(wizard_name))
            self.show_available_wizards()
        else:
            wizard: AbstractWizard = self._wizards.get(wizard_name)
            wizard.run()

    def _prepare_available_wizards_help(self) -> str:

        help_text: str = ""
        for name in self._wizards.keys():
            help_text = _WIZARD_HELP_TEXT_LINE.format(help_text, name, self._wizards.get(name).get_wizard_description())

        return help_text
