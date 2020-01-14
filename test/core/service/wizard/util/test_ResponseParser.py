import unittest
from unittest import mock

from core.service.wizard.step.BaseWizardStep import BaseWizardStep
from core.service.wizard.step.MultiAnswerWizardStepDecorator import MultiAnswerWizardStepDecorator
from core.service.wizard.step.OptionSelectorWizardStep import OptionSelectorWizardStep
from core.service.wizard.util.ResponseParser import ResponseParser
from test.core.service.wizard.step.TestWizardDataMapping import TestWizardDataMapping

_MULTI_ANSWER_STEP_SIDE_EFFECT = ["answer1", "answer2", "answer3", ""]

_TEST_SINGLE_RESPONSE = "test_single_response"
_WIZARD_STEP_FIELD = TestWizardDataMapping.TEST_MAPPING.get_wizard_field()


class ResponseParserTest(unittest.TestCase):

    def setUp(self) -> None:
        self.base_wizard_step_mock: BaseWizardStep = BaseWizardStep(TestWizardDataMapping.TEST_MAPPING, "test-question-1")
        self.option_selector_wizard_step_mock: OptionSelectorWizardStep = OptionSelectorWizardStep(TestWizardDataMapping.TEST_MAPPING, "test-question-2")
        self.multi_answer_wizard_step_mock: MultiAnswerWizardStepDecorator = MultiAnswerWizardStepDecorator(self.base_wizard_step_mock)

        self.response_parser: ResponseParser = ResponseParser()

    @mock.patch("builtins.input", return_value=_TEST_SINGLE_RESPONSE)
    def test_should_read_answer_for_base_wizard_step(self, input_mock):

        # given
        response_dict = {}

        # when
        self.response_parser.read_answer(self.base_wizard_step_mock, response_dict)

        # then
        self.assertEqual(response_dict[_WIZARD_STEP_FIELD], _TEST_SINGLE_RESPONSE)

    @mock.patch("builtins.input", return_value=2)
    def test_should_read_answer_for_option_selector_step_with_proper_value(self, input_mock):

        # given
        response_dict = {}

        # when
        self.response_parser.read_answer(self.option_selector_wizard_step_mock, response_dict)

        # then
        self.assertEqual(response_dict[_WIZARD_STEP_FIELD], "no")

    @mock.patch("builtins.input", side_effect=[5, -1, 0, "test", 1])
    def test_should_read_answer_for_option_selector_step_with_multiple_consequent_mistakes(self, input_mock):

        # given
        response_dict = {}

        # when
        self.response_parser.read_answer(self.option_selector_wizard_step_mock, response_dict)

        # then
        self.assertEqual(response_dict[_WIZARD_STEP_FIELD], "yes")

    @mock.patch("builtins.input", side_effect=_MULTI_ANSWER_STEP_SIDE_EFFECT)
    def test_should_read_answer_for_multi_answer_step(self, input_mock):

        # given
        response_dict = {}

        # when
        self.response_parser.read_answer(self.multi_answer_wizard_step_mock, response_dict)

        # then
        self.assertEqual(response_dict[_WIZARD_STEP_FIELD], _MULTI_ANSWER_STEP_SIDE_EFFECT[0:-1])


if __name__ == "__main__":
    unittest.main()
