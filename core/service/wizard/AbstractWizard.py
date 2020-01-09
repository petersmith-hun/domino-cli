from abc import ABCMeta, abstractmethod
from typing import List, Iterator, Optional

from core.service.wizard.step.MultiAnswerWizardStepDecorator import MultiAnswerWizardStepDecorator
from core.service.wizard.step.WizardStep import WizardStep, WizardStepTransition


class AbstractWizard(object, metaclass=ABCMeta):

    def __init__(self, wizard_name: str):
        self._wizard_name = wizard_name
        self._entry_point = None
        self._init_wizard()

    def get_wizard_name(self):
        return self._wizard_name

    def set_entry_point(self, entry_point: WizardStep):
        self._entry_point = entry_point

    def run(self) -> None:

        result: dict = {}
        current_step: WizardStep = self._get_entry_point()

        while True:

            print(current_step)
            AbstractWizard._read_answer(current_step, result)
            current_step = AbstractWizard._get_next_step(current_step, result)

            if current_step is None:
                break

        self._handle_result(result)

    def _get_entry_point(self) -> WizardStep:

        if self._entry_point is None:
            raise Exception("Incorrectly configured wizard - entry point is none")

        return self._entry_point

    @staticmethod
    def _read_answer(current_step: WizardStep, result: dict) -> None:

        if type(current_step) is MultiAnswerWizardStepDecorator:
            result[current_step.get_step_id()] = []
            while True:
                current_answer = input()
                if len(current_answer) > 0:
                    result[current_step.get_step_id()].append(current_answer)
                else:
                    break
        else:
            result[current_step.get_step_id()] = input()

    @staticmethod
    def _get_next_step(current_step: WizardStep, result: dict) -> Optional[WizardStep]:

        next_step: Optional[WizardStep] = None

        transitions: List[WizardStepTransition] = current_step.get_transitions()
        if len(transitions) > 0:
            possible_next_steps: Iterator[WizardStepTransition] = filter(lambda step: step.is_applicable(result), transitions)
            selected_next_step: WizardStepTransition = next(possible_next_steps, None)

            if selected_next_step is not None:
                next_step = selected_next_step.get_wizard_step()

        return next_step

    @abstractmethod
    def _init_wizard(self) -> None:
        pass

    @abstractmethod
    def _handle_result(self, result: dict):
        pass
