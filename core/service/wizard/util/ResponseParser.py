from core.service.wizard.step.MultiAnswerWizardStepDecorator import MultiAnswerWizardStepDecorator
from core.service.wizard.step.OptionSelectorWizardStep import OptionSelectorWizardStep
from core.service.wizard.step.WizardStep import WizardStep


class ResponseParser:

    def read_answer(self, current_step: WizardStep, result: dict) -> None:

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

            answer = current_step.get_options()[index]

        return answer
