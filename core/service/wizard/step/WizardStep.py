from __future__ import annotations
from abc import ABCMeta, abstractmethod
from typing import List, Callable

_DEFAULT_APPLICABILITY_PREDICATE = (lambda context: True)


class WizardStep(object, metaclass=ABCMeta):
    """
    Wizard step interface. Wizard steps are basically the "questions" stated by the wizard with the configured
    transitions to the next steps.
    """
    @abstractmethod
    def get_step_id(self) -> str:
        """
        Returns the set step ID. This will be used as the field name in the source (raw response) dictionary.

        :return: set step ID (raw response field name)
        """
        pass

    @abstractmethod
    def get_transitions(self) -> List[WizardStepTransition]:
        """
        Returns the list of possible transitions from this wizard step.

        :return: list of possible transitions from this wizard step
        """
        pass

    @abstractmethod
    def add_transition(self, wizard_step: WizardStep, applicability_predicate: Callable[[dict], bool] = None) -> None:
        """
        Adds a possible transition for this wizard step.
        Need to specify the target wizard step and the applicability predicate, which is used for deciding if it is
        possible to transition into the specified step from this one based on the current response context.

        :param wizard_step: target WizardStep
        :param applicability_predicate: decision logic that determines if the transition is possible (defaults to None)
        """
        pass


class WizardStepTransition:
    """
    Wizard step transition definition.
    Holds a target WizardStep with its applicability predicate.
    Applicability predicate defaults to 'context: True' (transition unconditionally) in case the specified one is None.
    """
    def __init__(self, wizard_step: WizardStep, applicability_predicate: Callable[[dict], bool]):
        self._wizard_step: WizardStep = wizard_step
        self._applicability_predicate: Callable[[dict], bool] = _DEFAULT_APPLICABILITY_PREDICATE \
            if applicability_predicate is None \
            else applicability_predicate

    def get_wizard_step(self) -> WizardStep:
        """
        Returns the held WizardStep object.

        :return: held WizardStep object
        """
        return self._wizard_step

    def is_applicable(self, context: dict) -> bool:
        """
        Executes the stored applicability predicate on the given response context (raw response dictionary).

        :param context: raw response dictionary
        :return: boolean True is the step is applicable (can be transitioned to), False otherwise
        """
        return self._applicability_predicate(context)
