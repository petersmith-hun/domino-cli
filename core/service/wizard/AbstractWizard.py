from abc import ABCMeta, abstractmethod
from typing import List, Iterator, Optional

from core.service.wizard.step.WizardStep import WizardStep, WizardStepTransition
from core.service.wizard.util.ResponseParser import ResponseParser


class AbstractWizard(object, metaclass=ABCMeta):
    """
    Wizard controller engine base implementation.
    Concrete wizards must implement this base implementation.
    """
    def __init__(self, response_parser: ResponseParser, wizard_name: str, wizard_description: str):
        self._response_parser = response_parser
        self._wizard_name: str = wizard_name
        self._wizard_description = wizard_description
        self._entry_point: Optional[WizardStep] = None
        self._init_wizard()

    def get_wizard_name(self) -> str:
        """
        Returns the name (ID) of this wizard.
        The specified name will be used by the CLI to execute this wizard.

        :return: name of this wizard
        """
        return self._wizard_name

    def get_wizard_description(self) -> str:
        """
        Returns the description of this wizard.

        :return: description of this wizard
        """
        return self._wizard_description

    def set_entry_point(self, entry_point: WizardStep) -> None:
        """
        Returns the entry point (the first step) of this wizard.
        This method must be called inside _init_wizard method with a configured WizardStep, otherwise wizard
        execution will fail because of missing entry point.

        :param entry_point: first WizardStep of this wizard
        """
        self._entry_point = entry_point

    def run(self) -> None:
        """
        Runs this wizard by executing the following steps:
         - [1] Retrieves the first step.
         - [2] Prints the step.
         - [3] Waits for the answer.
         - [4] Extracts the next step.
               If there is one, goes back to point [2].
         - [5] It there's no more wizard steps, starts compiling the result.
        """
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
        """
        Returns set entry point (first WizardStep) or raises exception in case it is missing.

        :return: set entry point
        """
        if self._entry_point is None:
            raise Exception("Incorrectly configured wizard - entry point is none")

        return self._entry_point

    def _get_next_step(self, current_step: WizardStep, result: dict) -> Optional[WizardStep]:
        """
        Returns the next WizardStep (in case there's any).
        Filters to the first possible (in the order of definition in _init_wizard method) WizardStep based on the set
        applicability predicates.

        :param current_step: current WizardStep to retrieve possible transitions
        :param result: raw response data dictionary (for applicability checks)
        :return: next WizardStep or None if there's either no more or none of them can be transitioned to
        """
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
        """
        This method must be implemented to configure the wizard.
        In the method body three things must be done:
         - Initializing wizard steps.
         - Defining transitions.
         - Setting entry point.
        """
        pass

    @abstractmethod
    def _handle_result(self, result: dict) -> None:
        """
        Implement this method to handle the raw response data dictionary.

        :param result: raw response data dictionary
        """
        pass
