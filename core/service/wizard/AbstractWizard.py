from abc import ABCMeta, abstractmethod
from typing import List, Iterator

from core.service.wizard.WizardStep import AbstractWizardStep, WizardStepTransition


class AbstractWizard(object, metaclass=ABCMeta):

    def __init__(self, wizard_name: str):
        self._wizard_name = wizard_name
        self._entry_point = None
        self._init_wizard()

    def get_wizard_name(self):
        return self._wizard_name

    def set_entry_point(self, entry_point: AbstractWizardStep):
        self._entry_point = entry_point

    def run(self) -> None:

        result: dict = {}
        current_step: AbstractWizardStep = self._get_entry_point()

        while True:
            print(current_step)
            result[current_step.step_id] = input()

            transitions: List[WizardStepTransition] = current_step.get_transitions()
            if len(transitions) == 0:
                break

            possible_next_steps: Iterator[WizardStepTransition] = filter(lambda step: step.is_applicable(result), transitions)
            selected_next_step: WizardStepTransition = next(possible_next_steps, None)

            if selected_next_step is None:
                break
            else:
                current_step = selected_next_step.get_wizard_step()

        self._handle_result(result)

    def _get_entry_point(self) -> AbstractWizardStep:

        if self._entry_point is None:
            raise Exception("Incorrectly configured wizard - entry point is none")

        return self._entry_point

    @abstractmethod
    def _init_wizard(self) -> None:
        pass

    @abstractmethod
    def _handle_result(self, result: dict):
        pass
