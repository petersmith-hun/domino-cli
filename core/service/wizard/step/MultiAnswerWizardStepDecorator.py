from typing import List, Callable

from core.service.wizard.step.WizardStep import WizardStep, WizardStepTransition


class MultiAnswerWizardStepDecorator(WizardStep):

    def __init__(self, wrapped_wizard_step: WizardStep):
        self._wrapped_wizard_step: WizardStep = wrapped_wizard_step

    def get_step_id(self) -> str:
        return self._wrapped_wizard_step.get_step_id()

    def get_transitions(self) -> List[WizardStepTransition]:
        return self._wrapped_wizard_step.get_transitions()

    def add_transition(self, wizard_step: WizardStep, applicability_predicate: Callable[[dict], bool] = None) -> None:
        return self._wrapped_wizard_step.add_transition(wizard_step, applicability_predicate)

    def __repr__(self):
        return self._wrapped_wizard_step.__repr__()
