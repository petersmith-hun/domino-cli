import unittest
from unittest import mock

from core.service.wizard.RegistrationConfigWizard import RegistrationConfigWizard
from core.service.wizard.render.WizardResultConsoleRenderer import WizardResultConsoleRenderer
from core.service.wizard.render.WizardResultFileRenderer import WizardResultFileRenderer
from core.service.wizard.transformer.AbstractWizardResultTransformer import AbstractWizardResultTransformer

_TRANSFORMED_VALUE = {"transformed": {}}

_EXECUTABLE_TYPE_RAW_RESPONSES = [
    "app1",
    "1",
    "1",
    "/home",
    "app1-exec.jar",
    "app_user",
    "--arg1",
    "--arg2",
    "",
    "1",
    "3 seconds",
    "2 seconds",
    2,
    "http://localhost:8099/health",
    "1"
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
    "1",
    "2",
    "/home",
    "app2-exec.jar",
    "java",
    "app_user",
    "--arg1",
    "",
    "2",
    "1"
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
    "1",
    "3",
    "/home",
    "app3-exec.jar",
    "app3-svc",
    "app_svc_user",
    "2",
    "2"
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

_DOCKER_STANDARD_TYPE_RAW_RESPONSES = [
    "app4",
    "2",
    "1",
    "http://localhost:5000/apps",
    "img_app4",
    "container_app4",
    "9000:9000/tcp",
    "8080:8080",
    "",
    "ENV_VAR1:value1",
    "ENV_VAR2:value2",
    "ENV_VAR3:value3",
    "",
    "/tmp1:/tmp1",
    "/tmp2/something:/app/tmp:rw",
    "/tmp3/tmp:/app/something:ro",
    "",
    "host",
    "4",
    "--param1",
    "--param2",
    "",
    "2",
    "1"
]
_DOCKER_STANDARD_TYPE_FORMATTED_RESPONSE_DICT: dict = {
    "reg_name": "app4",
    "source_type": "docker",
    "exec_type": "standard",
    "src_home": "http://localhost:5000/apps",
    "src_bin_name": "img_app4",
    "exec_cmd_name": "container_app4",
    "exec_args_docker_ports": {
        "9000": "9000/tcp",
        "8080": "8080"
    },
    "exec_args_docker_env": {
        "ENV_VAR1": "value1",
        "ENV_VAR2": "value2",
        "ENV_VAR3": "value3"
    },
    "exec_args_docker_volumes": {
        "/tmp1": "/tmp1",
        "/tmp2/something": "/app/tmp:rw",
        "/tmp3/tmp": "/app/something:ro"
    },
    "exec_args_docker_network": "host",
    "exec_args_docker_restart": "unless-stopped",
    "exec_args_docker_cmd": [
        "--param1",
        "--param2"
    ],
    "hc_enable": "no",
    "result_rendering": "console"
}


class RegistrationConfigWizardTest(unittest.TestCase):

    def setUp(self) -> None:
        self.wizard_result_transformer_mock: AbstractWizardResultTransformer = mock.create_autospec(AbstractWizardResultTransformer)
        self.wizard_result_console_renderer_mock: WizardResultConsoleRenderer = mock.create_autospec(WizardResultConsoleRenderer)
        self.wizard_result_file_renderer_mock: WizardResultFileRenderer = mock.create_autospec(WizardResultFileRenderer)

        self.wizard_result_transformer_mock.transform.return_value = _TRANSFORMED_VALUE

        self.registration_config_wizard: RegistrationConfigWizard = RegistrationConfigWizard(
            self.wizard_result_transformer_mock,
            self.wizard_result_console_renderer_mock,
            self.wizard_result_file_renderer_mock)

    @mock.patch("builtins.input", side_effect=_EXECUTABLE_TYPE_RAW_RESPONSES)
    def test_should_run_wizard_for_executable_type_and_console_rendering(self, input_mock):

        # when
        self.registration_config_wizard.run()

        # then
        self.wizard_result_transformer_mock.transform.assert_called_once_with(_EXECUTABLE_TYPE_FORMATTED_RESPONSE_DICT)
        self.wizard_result_console_renderer_mock.render.assert_called_once_with(_TRANSFORMED_VALUE)

    @mock.patch("builtins.input", side_effect=_RUNTIME_TYPE_RAW_RESPONSES)
    def test_should_run_wizard_for_runtime_type_and_console_rendering(self, input_mock):

        # when
        self.registration_config_wizard.run()

        # then
        self.wizard_result_transformer_mock.transform.assert_called_once_with(_RUNTIME_TYPE_FORMATTED_RESPONSE_DICT)
        self.wizard_result_console_renderer_mock.render.assert_called_once_with(_TRANSFORMED_VALUE)

    @mock.patch("builtins.input", side_effect=_SERVICE_TYPE_RAW_RESPONSES)
    def test_should_run_wizard_for_service_type_and_file_rendering(self, input_mock):

        # when
        self.registration_config_wizard.run()

        # then
        file_renderer_call_args = self.wizard_result_file_renderer_mock.render.call_args.args
        merge_lambda_result = file_renderer_call_args[1]({"domino": {"registrations": {"key": "value"}}})

        self.wizard_result_transformer_mock.transform.assert_called_once_with(_SERVICE_TYPE_FORMATTED_RESPONSE_DICT)
        self.assertEqual(file_renderer_call_args[0], _TRANSFORMED_VALUE)
        self.assertEqual(merge_lambda_result, {"key": "value"})

    @mock.patch("builtins.input", side_effect=_DOCKER_STANDARD_TYPE_RAW_RESPONSES)
    def test_should_run_wizard_for_docker_standard_type_and_console_rendering(self, input_mock):

        # when
        self.registration_config_wizard.run()

        # then
        self.wizard_result_transformer_mock.transform.assert_called_once_with(_DOCKER_STANDARD_TYPE_FORMATTED_RESPONSE_DICT)
        self.wizard_result_console_renderer_mock.render.assert_called_once_with(_TRANSFORMED_VALUE)


if __name__ == "__main__":
    unittest.main()
