from __future__ import annotations
from abc import ABCMeta, abstractmethod
from typing import List, Callable

_DEFAULT_APPLICABILITY_PREDICATE = (lambda context: True)


class WizardStep(object, metaclass=ABCMeta):

    @abstractmethod
    def get_step_id(self) -> str:
        pass

    @abstractmethod
    def get_transitions(self) -> List[WizardStepTransition]:
        pass

    @abstractmethod
    def add_transition(self, wizard_step: WizardStep, applicability_predicate: Callable[[dict], bool] = None) -> None:
        pass


class WizardStepTransition:

    def __init__(self, wizard_step: WizardStep, applicability_predicate: Callable[[dict], bool]):
        self._wizard_step: WizardStep = wizard_step
        self._applicability_predicate: Callable[[dict], bool] = _DEFAULT_APPLICABILITY_PREDICATE \
            if applicability_predicate is None \
            else applicability_predicate

    def get_wizard_step(self) -> WizardStep:
        return self._wizard_step

    def is_applicable(self, context: dict) -> bool:
        return self._applicability_predicate(context)
