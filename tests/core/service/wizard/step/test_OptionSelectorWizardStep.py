import unittest
from typing import List
from unittest import mock

from domino_cli.core.service.wizard.step.OptionSelectorWizardStep import OptionSelectorWizardStep
from tests.core.service.wizard.step.TestWizardDataMapping import TestWizardDataMapping

_TEST_QUESTION = "test_question"
_WIZARD_STEP_FIELD = TestWizardDataMapping.TEST_MAPPING.get_wizard_field()


class OptionSelectorWizardStepTest(unittest.TestCase):

    def test_should_get_default_options(self):

        # given
        option_selector_wizard_step: OptionSelectorWizardStep = OptionSelectorWizardStep(TestWizardDataMapping.TEST_MAPPING, _TEST_QUESTION)

        # when
        result: List[str] = option_selector_wizard_step.get_options()

        # then
        self.assertEqual(result, ["yes", "no"])

    def test_should_get_specified_options(self):

        # given
        options = ["opt1", "opt2", "opt3"]
        option_selector_wizard_step: OptionSelectorWizardStep = OptionSelectorWizardStep(TestWizardDataMapping.TEST_MAPPING, _TEST_QUESTION, options)

        # when
        result: List[str] = option_selector_wizard_step.get_options()

        # then
        self.assertEqual(result, options)

    @mock.patch("builtins.input", return_value="2")
    def test_should_read_answer_with_proper_value(self, input_mock):

        # given
        response_dict = {}
        option_selector_wizard_step: OptionSelectorWizardStep = OptionSelectorWizardStep(TestWizardDataMapping.TEST_MAPPING, _TEST_QUESTION)

        # when
        option_selector_wizard_step.read_answer(response_dict)

        # then
        self.assertEqual(response_dict[_WIZARD_STEP_FIELD], "no")

    @mock.patch("builtins.input", side_effect=["5", "-1", "0", "test", "1"])
    def test_should_read_answer_with_multiple_consequent_mistakes(self, input_mock):

        # given
        response_dict = {}
        option_selector_wizard_step: OptionSelectorWizardStep = OptionSelectorWizardStep(TestWizardDataMapping.TEST_MAPPING, _TEST_QUESTION)

        # when
        option_selector_wizard_step.read_answer(response_dict)

        # then
        self.assertEqual(response_dict[_WIZARD_STEP_FIELD], "yes")

    def test_should_repr_show_options_formatted(self):

        # given
        option_selector_wizard_step: OptionSelectorWizardStep = OptionSelectorWizardStep(TestWizardDataMapping.TEST_MAPPING, _TEST_QUESTION)

        # when
        result: str = option_selector_wizard_step.__repr__()

        # then
        self.assertEqual(result, "test_question  \n\t [1] yes \n\t [2] no")


if __name__ == "__main__":
    unittest.main()
