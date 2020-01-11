from abc import ABCMeta, abstractmethod
from typing import List, Iterator, Optional

from core.service.wizard.step.WizardStep import WizardStep, WizardStepTransition
from core.service.wizard.util.ResponseParser import ResponseParser


class AbstractWizard(object, metaclass=ABCMeta):

    def __init__(self, response_parser: ResponseParser, wizard_name: str, wizard_description: str):
        self._response_parser = response_parser
        self._wizard_name: str = wizard_name
        self._wizard_description = wizard_description
        self._entry_point: Optional[WizardStep] = None
        self._init_wizard()

    def get_wizard_name(self) -> str:
        return self._wizard_name

    def get_wizard_description(self) -> str:
        return self._wizard_description

    def set_entry_point(self, entry_point: WizardStep):
        self._entry_point = entry_point

    def run(self) -> None:

        result: dict = {}
        current_step: WizardStep = self._get_entry_point()

        while True:

            print(current_step)
            self._response_parser.read_answer(current_step, result)
            current_step = self._get_next_step(current_step, result)

            if current_step is None:
                break

        self._handle_result(result)

    def _get_entry_point(self) -> WizardStep:

        if self._entry_point is None:
            raise Exception("Incorrectly configured wizard - entry point is none")

        return self._entry_point

    def _get_next_step(self, current_step: WizardStep, result: dict) -> Optional[WizardStep]:

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
    def _handle_result(self, result: dict) -> None:
        pass
