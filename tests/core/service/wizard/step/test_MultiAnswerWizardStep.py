import unittest
from unittest import mock

from domino_cli.core.service.wizard.step.MultiAnswerWizardStep import MultiAnswerWizardStep
from tests.core.service.wizard.step.TestWizardDataMapping import TestWizardDataMapping

_TEST_MULTI_RESPONSE = "test_multi_response"
_MULTI_ANSWER_STEP_SIDE_EFFECT = ["answer1", "answer2", "answer3", ""]
_WIZARD_STEP_FIELD = TestWizardDataMapping.TEST_MAPPING.get_wizard_field()


class MultiAnswerWizardStepTest(unittest.TestCase):

    def setUp(self) -> None:
        self.multi_answer_wizard_step: MultiAnswerWizardStep = MultiAnswerWizardStep(TestWizardDataMapping.TEST_MAPPING, _TEST_MULTI_RESPONSE)

    @mock.patch("builtins.input", side_effect=_MULTI_ANSWER_STEP_SIDE_EFFECT)
    def test_should_read_answer_for_multi_answer_step(self, input_mock):

        # given
        response_dict = {}

        # when
        self.multi_answer_wizard_step.read_answer(response_dict)

        # then
        self.assertEqual(response_dict[_WIZARD_STEP_FIELD], _MULTI_ANSWER_STEP_SIDE_EFFECT[0:-1])

    def test_should_repr_return_assigned_question(self):

        # when
        result: str = self.multi_answer_wizard_step.__repr__()

        # then
        self.assertEqual(result, "{0} (one at a line, empty line to stop)".format(_TEST_MULTI_RESPONSE))


if __name__ == "__main__":
    unittest.main()
