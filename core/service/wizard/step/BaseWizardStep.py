from typing import List, Callable

from core.service.wizard.mapping.WizardDataMappingBaseEnum import WizardDataMappingBaseEnum
from core.service.wizard.step.WizardStep import WizardStep, WizardStepTransition


class BaseWizardStep(WizardStep):

    def __init__(self, step_id: WizardDataMappingBaseEnum, question: str):
        self._step_id: str = step_id.get_wizard_field()
        self._question: str = question
        self._transitions: List[WizardStepTransition] = []

    def get_step_id(self) -> str:
        return self._step_id

    def get_transitions(self) -> List[WizardStepTransition]:
        return self._transitions

    def add_transition(self, wizard_step: WizardStep, applicability_predicate: Callable[[dict], bool] = None) -> None:
        self._transitions.append(WizardStepTransition(wizard_step, applicability_predicate))

    def __repr__(self):
        return self._question
