from typing import cast

from core.service.wizard.step.MultiAnswerWizardStepDecorator import MultiAnswerWizardStepDecorator
from core.service.wizard.step.OptionSelectorWizardStep import OptionSelectorWizardStep
from core.service.wizard.step.WizardStep import WizardStep


class ResponseParser:
    """
    Component that reads a raw response based on the wizard step.
    """

    def read_answer(self, current_step: WizardStep, result: dict) -> None:
        """
        Reads a raw response.
        Uses the type of the WizardStep to decide how to read user input.
        The following methods are used:

         - Standard WizardStep (BaseWizardStep):
           Single answer is expected from stdin.

         - MultiAnswerWizardStepDecorator:
           Multiple answers are expected from stdin until an empty line is provided.

         - OptionSelectorWizardStep:
           Answer must be an integer (n > 0 and n < number of possible choices). Answer is validated,
           providing incorrect value restarts step. Can also be combined with MultiAnswerWizardStepDecorator.

        :param current_step: WizardStep object currently being executed, use for deciding the type of step
        :param result: raw response dictionary object to store response(s)
        """
        try:
            if type(current_step) is MultiAnswerWizardStepDecorator:
                result[current_step.get_step_id()] = []
                while True:
                    current_answer = self._read_answer_with_mapping(current_step)
                    if len(current_answer) > 0:
                        result[current_step.get_step_id()].append(current_answer)
                    else:
                        break
            else:
                result[current_step.get_step_id()] = self._read_answer_with_mapping(current_step)
        except (IndexError, ValueError):
            print("Your choice is invalid - please try again")
            self.read_answer(current_step, result)

    def _read_answer_with_mapping(self, current_step: WizardStep) -> str:

        answer: str = input()

        if type(current_step) is OptionSelectorWizardStep:
            index: int = int(answer) - 1

            if index < 0:
                raise ValueError()

            answer = cast(OptionSelectorWizardStep, current_step).get_options()[index]

        return answer
