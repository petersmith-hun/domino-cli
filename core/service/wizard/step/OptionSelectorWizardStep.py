from typing import List

from core.service.wizard.mapping.WizardDataMappingBaseEnum import WizardDataMappingBaseEnum
from core.service.wizard.step.BaseWizardStep import BaseWizardStep

_DEFAULT_OPTIONS = ["yes", "no"]


class OptionSelectorWizardStep(BaseWizardStep):

    def __init__(self, step_id: WizardDataMappingBaseEnum, question: str, options: List[str] = None):
        super().__init__(step_id, question)

        if options is None:
            options = _DEFAULT_OPTIONS

        self._options: List[str] = options

    def get_options(self) -> List[str]:
        return self._options

    def __repr__(self):
        return "{0} {1}".format(self._question, self._format_options())

    def _format_options(self) -> str:

        formatted_options: str = ""
        for index in range(0, len(self._options)):
            formatted_options = "{0} {1} [{2}] {3}".format(formatted_options, "\n\t", index + 1, self._options[index])

        return formatted_options
