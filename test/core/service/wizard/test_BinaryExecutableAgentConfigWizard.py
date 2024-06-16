import unittest
from unittest import mock

from core.service.wizard.BinaryExecutableAgentConfigWizard import BinaryExecutableAgentConfigWizard
from core.service.wizard.render.WizardResultConsoleRenderer import WizardResultConsoleRenderer
from core.service.wizard.render.WizardResultFileRenderer import WizardResultFileRenderer
from core.service.wizard.transformer.AbstractWizardResultTransformer import AbstractWizardResultTransformer

_TRANSFORMED_VALUE = {"transformed": {}}

_DEFAULTS_NO_RUNTIME_RAW_RESPONSES = [
    "",
    "coordinator-api-key",
    "5 minutes",
    "2 seconds",
    "devlocal",
    "1",
    "agent-key-1",
    "3",
    "1",
    "1",
    "3 seconds",
    "leaflet",
    "domino",
    "",
    "",
    "",
    "2",
    "1"
]
_DEFAULTS_NO_RUNTIME_FORMATTED_RESPONSE_DICT: dict = {
    "coordinator_host": "ws://127.0.0.1:9987/agent",
    "coordinator_api_key": "coordinator-api-key",
    "coordinator_ping": "5 minutes",
    "coordinator_pong": "2 seconds",
    "identification_host_id": "devlocal",
    "identification_type": "docker",
    "identification_agent_key": "agent-key-1",
    "logging_min_level": "warn",
    "logging_json": "yes",
    "spawn_control_service_handler": "systemd",
    "spawn_control_start_delay": "3 seconds",
    "spawn_control_exec_users": [
        "leaflet",
        "domino"
    ],
    "storage_deployments_store": "./storage/deployments",
    "storage_app_home": "./storage/home",
    "runtime_configure_first": "no",
    "result_rendering": "console"
}

_CUSTOM_AND_RUNTIME_CONFIG_RAW_RESPONSES = [
    "ws://192.168.0.1:7755/agent",
    "coordinator-api-key-2",
    "10 minutes",
    "3 seconds",
    "remote1",
    "2",
    "agent-key-2",
    "2",
    "2",
    "1",
    "5 seconds",
    "leaflet",
    "",
    "/opt/storage/deployments",
    "/opt/storage/home",
    "1",
    "java",
    "/bin/java",
    "--version",
    "{args} -jar {resource}",
    "2"
]
_CUSTOM_AND_RUNTIME_CONFIG_FORMATTED_RESPONSE_DICT: dict = {
    "coordinator_host": "ws://192.168.0.1:7755/agent",
    "coordinator_api_key": "coordinator-api-key-2",
    "coordinator_ping": "10 minutes",
    "coordinator_pong": "3 seconds",
    "identification_host_id": "remote1",
    "identification_type": "filesystem",
    "identification_agent_key": "agent-key-2",
    "logging_min_level": "info",
    "logging_json": "no",
    "spawn_control_service_handler": "systemd",
    "spawn_control_start_delay": "5 seconds",
    "spawn_control_exec_users": [
        "leaflet"
    ],
    "storage_deployments_store": "/opt/storage/deployments",
    "storage_app_home": "/opt/storage/home",
    "runtime_configure_first": "yes",
    "runtime_id": "java",
    "runtime_binary_path": "/bin/java",
    "runtime_healthcheck": "--version",
    "runtime_command_line": "{args} -jar {resource}",
    "result_rendering": "file"
}


class BinaryExecutableAgentConfigWizardTest(unittest.TestCase):

    def setUp(self) -> None:
        self.wizard_result_transformer_mock: AbstractWizardResultTransformer = mock.create_autospec(AbstractWizardResultTransformer)
        self.wizard_result_console_renderer_mock: WizardResultConsoleRenderer = mock.create_autospec(WizardResultConsoleRenderer)
        self.wizard_result_file_renderer_mock: WizardResultFileRenderer = mock.create_autospec(WizardResultFileRenderer)

        self.wizard_result_transformer_mock.transform.return_value = _TRANSFORMED_VALUE

        self.binary_executable_agent_config_wizard: BinaryExecutableAgentConfigWizard = BinaryExecutableAgentConfigWizard(
            self.wizard_result_transformer_mock,
            self.wizard_result_console_renderer_mock,
            self.wizard_result_file_renderer_mock)

    @mock.patch("builtins.input", side_effect=_DEFAULTS_NO_RUNTIME_RAW_RESPONSES)
    def test_should_run_wizard_for_configuration_with_defaults_and_no_runtime_and_console_rendering(self, _):

        # when
        self.binary_executable_agent_config_wizard.run()

        # then
        self.wizard_result_transformer_mock.transform.assert_called_once_with(_DEFAULTS_NO_RUNTIME_FORMATTED_RESPONSE_DICT)
        self.wizard_result_console_renderer_mock.render.assert_called_once_with(_TRANSFORMED_VALUE)

    @mock.patch("builtins.input", side_effect=_CUSTOM_AND_RUNTIME_CONFIG_RAW_RESPONSES)
    def test_should_run_wizard_for_configuration_with_runtime_config_and_file_rendering(self, _):

        # when
        self.binary_executable_agent_config_wizard.run()

        # then
        file_renderer_call_args = self.wizard_result_file_renderer_mock.render.call_args.args
        merge_lambda_result = file_renderer_call_args[1]({"domino": {"key": "value"}})

        self.wizard_result_transformer_mock.transform.assert_called_once_with(_CUSTOM_AND_RUNTIME_CONFIG_FORMATTED_RESPONSE_DICT)
        self.assertEqual(file_renderer_call_args[0], _TRANSFORMED_VALUE)
        self.assertEqual(merge_lambda_result, {"key": "value"})


if __name__ == "__main__":
    unittest.main()
