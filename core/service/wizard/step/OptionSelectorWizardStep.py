from core.service.wizard.mapping.WizardDataMappingBaseEnum import WizardDataMappingBaseEnum
from core.service.wizard.step.BaseWizardStep import BaseWizardStep

_DEFAULT_OPTIONS = ["yes", "no"]


class OptionSelectorWizardStep(BaseWizardStep):

    def __init__(self, step_id: WizardDataMappingBaseEnum, question: str, options: [] = None):
        super().__init__(step_id, question)

        if options is None:
            options = _DEFAULT_OPTIONS

        self.options = options

    def __repr__(self):
        return "{0} {1}".format(self._question, self.options)
