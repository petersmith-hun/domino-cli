from typing import List, Dict

from core.service.wizard.AbstractWizard import AbstractWizard


class ConfigurationWizardService:

    def __init__(self, wizards: List[AbstractWizard]):
        self._wizards: Dict[str, AbstractWizard] = {wizard.get_wizard_name(): wizard for wizard in wizards}
        self._available_wizards_help: str = self._prepare_available_wizards_help()

    def show_available_wizards(self) -> None:
        print("Available wizards:{0}".format(self._available_wizards_help))

    def run_wizard(self, wizard_name: str) -> None:

        if wizard_name not in self._wizards.keys():
            print("Unknown wizard '{0}'".format(wizard_name))
            self.show_available_wizards()
        else:
            wizard: AbstractWizard = self._wizards.get(wizard_name)
            wizard.run()

    def _prepare_available_wizards_help(self) -> str:

        help_text: str = ""
        for name in self._wizards.keys():
            help_text = "{}\n[{:>15}]: {}".format(help_text, name, self._wizards.get(name).get_wizard_description())

        return help_text
