import unittest
from typing import List
from unittest import mock

from domino_cli.core.service.wizard.step.BaseWizardStep import BaseWizardStep
from domino_cli.core.service.wizard.step.WizardStep import WizardStepTransition, WizardStep
from tests.core.service.wizard.step.TestWizardDataMapping import TestWizardDataMapping

_TEST_QUESTION = "test_question"
_TEST_SINGLE_RESPONSE = "test_single_response"
_WIZARD_STEP_FIELD = TestWizardDataMapping.TEST_MAPPING.get_wizard_field()


class BaseWizardStepTest(unittest.TestCase):

    def setUp(self) -> None:
        self.transition_step: WizardStep = mock.create_autospec(WizardStep)
        self.base_wizard_step: BaseWizardStep = BaseWizardStep(TestWizardDataMapping.TEST_MAPPING, _TEST_QUESTION)

    def test_should_get_step_id_return_mapping_wizard_field(self):

        # when
        result: str = self.base_wizard_step.get_step_id()

        # then
        self.assertEqual(result, TestWizardDataMapping.TEST_MAPPING.get_wizard_field())

    def test_should_handle_transitions(self):

        # given
        context_transitionable: dict = {"transition": "okay"}
        context_non_transitionable: dict = {"transition": "not_okay"}
        self.base_wizard_step.add_transition(self.transition_step)  # default transition
        self.base_wizard_step.add_transition(self.transition_step, lambda context: context["transition"] == "okay")

        # when
        result: List[WizardStepTransition] = self.base_wizard_step.get_transitions()

        # then
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].get_wizard_step(), self.transition_step)
        self.assertEqual(result[1].get_wizard_step(), self.transition_step)
        self.assertTrue(result[0].is_applicable(context_transitionable))
        self.assertTrue(result[0].is_applicable(context_non_transitionable))  # defaults transition is unconditional
        self.assertTrue(result[1].is_applicable(context_transitionable))
        self.assertFalse(result[1].is_applicable(context_non_transitionable))

    @mock.patch("builtins.input", return_value=_TEST_SINGLE_RESPONSE)
    def test_should_read_answer(self, input_mock):

        # given
        response_dict = {}

        # when
        self.base_wizard_step.read_answer(response_dict)

        # then
        self.assertEqual(response_dict[_WIZARD_STEP_FIELD], _TEST_SINGLE_RESPONSE)

    def test_should_repr_return_assigned_question(self):

        # when
        result: str = self.base_wizard_step.__repr__()

        # then
        self.assertEqual(result, _TEST_QUESTION)


if __name__ == "__main__":
    unittest.main()
