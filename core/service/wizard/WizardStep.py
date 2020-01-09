from typing import List


class AbstractWizardStep:

    def __init__(self, step_id: str, question: str):
        self.step_id: str = step_id
        self.question: str = question
        self._transitions: List[WizardStepTransition] = []

    def get_transitions(self):
        return self._transitions

    def add_transition(self, wizard_step, applicability_predicate=lambda context: True) -> None:
        self._transitions.append(WizardStepTransition(wizard_step, applicability_predicate))

    def __repr__(self):
        return self.question


class OptionSelectorWizardStep(AbstractWizardStep):

    def __init__(self, step_id: str, question: str, options: [] = None):
        super().__init__(step_id, question)

        if options is None:
            options = ["yes", "no"]

        self.options = options

    def __repr__(self):
        return "{0} {1}".format(self.question, self.options)


class CustomAnswerWizardStep(AbstractWizardStep):

    def __init__(self, step_id: str, question: str):
        super().__init__(step_id, question)


class WizardStepTransition:

    def __init__(self, wizard_step, applicability_predicate):
        self._wizard_step = wizard_step
        self._applicability_predicate = applicability_predicate

    def get_wizard_step(self):
        return self._wizard_step

    def is_applicable(self, context: dict):
        return self._applicability_predicate(context)
