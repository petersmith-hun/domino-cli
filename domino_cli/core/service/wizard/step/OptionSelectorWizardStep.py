from typing import List

from domino_cli.core.cli.Logging import warning
from domino_cli.core.service.wizard.mapping.WizardDataMappingBaseEnum import WizardDataMappingBaseEnum
from domino_cli.core.service.wizard.step.BaseWizardStep import BaseWizardStep

_DEFAULT_OPTIONS = ["yes", "no"]


class OptionSelectorWizardStep(BaseWizardStep):
    """
    BaseWizardStep extension for wizard steps specifying explicit response options.
    List of options can be emitted, in which case it defaults to yes/no.
    """
    def __init__(self, step_id: WizardDataMappingBaseEnum, question: str, options: List[str] = None):
        super().__init__(step_id, question)

        if options is None:
            options = _DEFAULT_OPTIONS

        self._options: List[str] = options

    def get_options(self) -> List[str]:
        """
        Returns the list of possible options.

        :return: list of possible options
        """
        return self._options

    def read_answer(self, result: dict) -> None:
        """
        Reads an answer from stdin. Answer must be an integer (n > 0 and n <= number of possible choices). Answer is
        validated, providing incorrect value restarts step.

        :param result: dictionary to be used to collect answers
        """
        try:
            super().read_answer(result)
            index: int = int(result[self.get_step_id()]) - 1

            if index < 0:
                raise ValueError()

            result[self.get_step_id()] = self.get_options()[index]

        except (IndexError, ValueError):
            warning("Your choice is invalid - please try again")
            self.read_answer(result)

    def __repr__(self):
        return "{0} {1}".format(self._question, self._format_options())

    def _format_options(self) -> str:

        formatted_options: str = ""
        for index in range(0, len(self._options)):
            formatted_options = "{0} {1} [{2}] {3}".format(formatted_options, "\n\t", index + 1, self._options[index])

        return formatted_options
