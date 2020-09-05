import unittest
from unittest import mock

from core.service.wizard.step.KeyValuePairAnswerWizardStep import KeyValuePairAnswerWizardStep
from test.core.service.wizard.step.TestWizardDataMapping import TestWizardDataMapping

_TEST_KEY_VALUE_RESPONSE = "test_key_value_response"
_KEY_VALUE_ANSWER_STEP_SIDE_EFFECT = ["key1:value1", "key2:value2", "key3", "key4:value4:additional_data", ""]
_WIZARD_STEP_FIELD = TestWizardDataMapping.TEST_MAPPING.get_wizard_field()


class KeyValuePairAnswerWizardStepTest(unittest.TestCase):

    def setUp(self) -> None:
        self.key_value_pair_answer_wizard_step: KeyValuePairAnswerWizardStep = KeyValuePairAnswerWizardStep(TestWizardDataMapping.TEST_MAPPING, _TEST_KEY_VALUE_RESPONSE)

    @mock.patch("builtins.input", side_effect=_KEY_VALUE_ANSWER_STEP_SIDE_EFFECT)
    def test_should_read_answer_for_multi_answer_step(self, input_mock):

        # given
        response_dict = {}
        expected_parsed_answer = {
            "key1": "value1",
            "key2": "value2",
            "key4": "value4:additional_data"
        }

        # when
        self.key_value_pair_answer_wizard_step.read_answer(response_dict)

        # then
        self.assertEqual(response_dict[_WIZARD_STEP_FIELD], expected_parsed_answer)

    def test_should_repr_return_assigned_question(self):

        # when
        result: str = self.key_value_pair_answer_wizard_step.__repr__()

        # then
        self.assertEqual(result, "{0} (in key:value format, empty line to stop)".format(_TEST_KEY_VALUE_RESPONSE))


if __name__ == "__main__":
    unittest.main()
