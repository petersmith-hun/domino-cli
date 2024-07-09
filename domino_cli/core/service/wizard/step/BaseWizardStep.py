from typing import List, Callable

from domino_cli.core.service.wizard.mapping.WizardDataMappingBaseEnum import WizardDataMappingBaseEnum
from domino_cli.core.service.wizard.step.WizardStep import WizardStep, WizardStepTransition


class BaseWizardStep(WizardStep):
    """
    Base WizardStep implementation providing common functionality of wizard steps.
    """
    def __init__(self, step_id: WizardDataMappingBaseEnum, question: str, default_answer: str = None):
        self._step_id: str = step_id.get_wizard_field()
        self._transitions: List[WizardStepTransition] = []
        self._default_answer: str = default_answer
        self._question: str = "{0} [default: {1}]".format(question, default_answer) \
            if default_answer is not None \
            else question

    def get_step_id(self) -> str:
        """
        See documentation of WizardStep.
        """
        return self._step_id

    def get_transitions(self) -> List[WizardStepTransition]:
        """
        See documentation of WizardStep.
        """
        return self._transitions

    def add_transition(self, wizard_step: WizardStep, applicability_predicate: Callable[[dict], bool] = None) -> None:
        """
        See documentation of WizardStep.
        """
        self._transitions.append(WizardStepTransition(wizard_step, applicability_predicate))

    def read_answer(self, result: dict) -> None:
        """
        See documentation of WizardStep.
        """
        answer: str = input()
        result[self.get_step_id()] = self._default_answer \
            if len(answer) == 0 \
            else answer

    def __repr__(self):
        return self._question
