import unittest
from unittest import mock

from core.service.wizard.RegistrationConfigWizard import RegistrationConfigWizard
from core.service.wizard.render.WizardResultConsoleRenderer import WizardResultConsoleRenderer
from core.service.wizard.render.WizardResultFileRenderer import WizardResultFileRenderer
from core.service.wizard.step.WizardStep import WizardStep
from core.service.wizard.transformer.AbstractWizardResultTransformer import AbstractWizardResultTransformer
from core.service.wizard.util.ResponseParser import ResponseParser

_TRANSFORMED_VALUE = {"transformed": {}}

_EXECUTABLE_TYPE_RAW_RESPONSES = [
    "app1",
    "filesystem",
    "executable",
    "/home",
    "app1-exec.jar",
    "app_user",
    [
        "--arg1",
        "--arg2"
    ],
    "yes",
    "3 seconds",
    "2 seconds",
    2,
    "http://localhost:8099/health",
    "console"
]
_EXECUTABLE_TYPE_FORMATTED_RESPONSE_DICT: dict = {
    "reg_name": "app1",
    "source_type": "filesystem",
    "exec_type": "executable",
    "src_home": "/home",
    "src_bin_name": "app1-exec.jar",
    "exec_user": "app_user",
    "exec_args": [
        "--arg1",
        "--arg2"
    ],
    "hc_enable": "yes",
    "hc_delay": "3 seconds",
    "hc_timeout": "2 seconds",
    "hc_max_attempts": 2,
    "hc_endpoint": "http://localhost:8099/health",
    "result_rendering": "console"
}

_RUNTIME_TYPE_RAW_RESPONSES = [
    "app2",
    "filesystem",
    "runtime",
    "/home",
    "app2-exec.jar",
    "java",
    "app_user",
    [
        "--arg1"
    ],
    "no",
    "console"
]
_RUNTIME_TYPE_FORMATTED_RESPONSE_DICT: dict = {
    "reg_name": "app2",
    "source_type": "filesystem",
    "exec_type": "runtime",
    "src_home": "/home",
    "src_bin_name": "app2-exec.jar",
    "runtime_name": "java",
    "exec_user": "app_user",
    "exec_args": [
        "--arg1"
    ],
    "hc_enable": "no",
    "result_rendering": "console"
}

_SERVICE_TYPE_RAW_RESPONSES = [
    "app3",
    "filesystem",
    "service",
    "/home",
    "app3-exec.jar",
    "app3-svc",
    "app_svc_user",
    "no",
    "file"
]
_SERVICE_TYPE_FORMATTED_RESPONSE_DICT: dict = {
    "reg_name": "app3",
    "source_type": "filesystem",
    "exec_type": "service",
    "src_home": "/home",
    "src_bin_name": "app3-exec.jar",
    "exec_cmd_name": "app3-svc",
    "exec_user": "app_svc_user",
    "hc_enable": "no",
    "result_rendering": "file"
}


class RegistrationConfigWizardTest(unittest.TestCase):

    def setUp(self) -> None:
        self.response_parser_mock: ResponseParser = mock.create_autospec(ResponseParser)
        self.wizard_result_transformer_mock: AbstractWizardResultTransformer = mock.create_autospec(AbstractWizardResultTransformer)
        self.wizard_result_console_renderer_mock: WizardResultConsoleRenderer = mock.create_autospec(WizardResultConsoleRenderer)
        self.wizard_result_file_renderer_mock: WizardResultFileRenderer = mock.create_autospec(WizardResultFileRenderer)

        self.response_index = 0
        self.wizard_result_transformer_mock.transform.return_value = _TRANSFORMED_VALUE

        self.registration_config_wizard: RegistrationConfigWizard = RegistrationConfigWizard(
            self.wizard_result_transformer_mock,
            self.wizard_result_console_renderer_mock,
            self.wizard_result_file_renderer_mock,
            self.response_parser_mock)

    def test_should_run_wizard_for_executable_type_and_console_rendering(self):

        # given
        self.response_parser_mock.read_answer.side_effect = self._response_parser_executable_side_effect

        # when
        self.registration_config_wizard.run()

        # then
        self.wizard_result_transformer_mock.transform.assert_called_once_with(_EXECUTABLE_TYPE_FORMATTED_RESPONSE_DICT)
        self.wizard_result_console_renderer_mock.render.assert_called_once_with(_TRANSFORMED_VALUE)

    def test_should_run_wizard_for_runtime_type_and_console_rendering(self):

        # given
        self.response_parser_mock.read_answer.side_effect = self._response_parser_runtime_side_effect

        # when
        self.registration_config_wizard.run()

        # then
        self.wizard_result_transformer_mock.transform.assert_called_once_with(_RUNTIME_TYPE_FORMATTED_RESPONSE_DICT)
        self.wizard_result_console_renderer_mock.render.assert_called_once_with(_TRANSFORMED_VALUE)

    def test_should_run_wizard_for_service_type_and_file_rendering(self):

        # given
        self.response_parser_mock.read_answer.side_effect = self._response_parser_service_side_effect

        # when
        self.registration_config_wizard.run()

        # then
        file_renderer_call_args = self.wizard_result_file_renderer_mock.render.call_args.args
        merge_lambda_result = file_renderer_call_args[1]({"domino": {"registrations": {"key": "value"}}})

        self.wizard_result_transformer_mock.transform.assert_called_once_with(_SERVICE_TYPE_FORMATTED_RESPONSE_DICT)
        self.assertEqual(file_renderer_call_args[0], _TRANSFORMED_VALUE)
        self.assertEqual(merge_lambda_result, {"key": "value"})

    def _response_parser_executable_side_effect(self, current_step: WizardStep, result: dict) -> None:
        self._response_parser_side_effect(_EXECUTABLE_TYPE_RAW_RESPONSES, current_step, result)

    def _response_parser_runtime_side_effect(self, current_step: WizardStep, result: dict) -> None:
        self._response_parser_side_effect(_RUNTIME_TYPE_RAW_RESPONSES, current_step, result)

    def _response_parser_service_side_effect(self, current_step: WizardStep, result: dict) -> None:
        self._response_parser_side_effect(_SERVICE_TYPE_RAW_RESPONSES, current_step, result)

    def _response_parser_side_effect(self, response_source: [], current_step: WizardStep, result: dict) -> None:
        result[current_step.get_step_id()] = response_source[self.response_index]
        self.response_index = self.response_index + 1


if __name__ == "__main__":
    unittest.main()
