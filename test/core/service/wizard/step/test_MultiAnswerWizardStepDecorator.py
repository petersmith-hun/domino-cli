import unittest
from unittest import mock

from core.service.wizard.step.MultiAnswerWizardStepDecorator import MultiAnswerWizardStepDecorator
from core.service.wizard.step.WizardStep import WizardStep


class MultiAnswerWizardStepDecoratorTest(unittest.TestCase):

    def setUp(self) -> None:
        self.wrapped_step: WizardStep = mock.create_autospec(WizardStep)
        self.transition_step: WizardStep = mock.create_autospec(WizardStep)
        self.applicability_predicate = lambda context: True

        self.multi_answer_wizard_step_decorator: MultiAnswerWizardStepDecorator = MultiAnswerWizardStepDecorator(self.wrapped_step)

    def test_should_get_step_id_by_calling_wrapped(self):

        # when
        self.multi_answer_wizard_step_decorator.get_step_id()

        # then
        self.assertEqual(self.wrapped_step.get_step_id.call_count, 1)

    def test_should_get_transitions_by_calling_wrapped(self):

        # when
        self.multi_answer_wizard_step_decorator.get_transitions()

        # then
        self.assertEqual(self.wrapped_step.get_transitions.call_count, 1)

    def test_should_add_transition_by_calling_wrapped(self):

        # when
        self.multi_answer_wizard_step_decorator.add_transition(self.transition_step, self.applicability_predicate)

        # then
        self.wrapped_step.add_transition.assert_called_once_with(self.transition_step, self.applicability_predicate)


if __name__ == "__main__":
    unittest.main()
