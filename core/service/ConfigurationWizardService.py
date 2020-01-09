from typing import List, Dict

from core.service.wizard.AbstractWizard import AbstractWizard


class ConfigurationWizardService:

    def __init__(self, wizards: List[AbstractWizard]):
        self._wizards: Dict[str, AbstractWizard] = {wizard.get_wizard_name(): wizard for wizard in wizards}

    def run_wizard(self):
        wizard: AbstractWizard = self._wizards.get("registration_config")  # TODO wizard name will be parameter from CommandDescriptor
        wizard.run()
