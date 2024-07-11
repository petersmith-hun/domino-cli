import unittest
from unittest import mock

from domino_cli.core.service.wizard.DockerAgentConfigWizard import DockerAgentConfigWizard
from domino_cli.core.service.wizard.render.WizardResultConsoleRenderer import WizardResultConsoleRenderer
from domino_cli.core.service.wizard.render.WizardResultFileRenderer import WizardResultFileRenderer
from domino_cli.core.service.wizard.transformer.AbstractWizardResultTransformer import AbstractWizardResultTransformer

_TRANSFORMED_VALUE = {"transformed": {}}

_DEFAULTS_NO_SERVER_RAW_RESPONSES = [
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
    "",
    "2",
    "1"
]
_DEFAULTS_NO_SERVER_FORMATTED_RESPONSE_DICT: dict = {
    "coordinator_host": "ws://127.0.0.1:9987/agent",
    "coordinator_api_key": "coordinator-api-key",
    "coordinator_ping": "5 minutes",
    "coordinator_pong": "2 seconds",
    "identification_host_id": "devlocal",
    "identification_type": "docker",
    "identification_agent_key": "agent-key-1",
    "logging_min_level": "warn",
    "logging_json": "yes",
    "docker_connection_type": "socket",
    "docker_connection_uri": "/var/run/docker.sock",
    "docker_registry_configure_first": "no",
    "result_rendering": "console"
}

_CUSTOM_AND_SERVER_CONFIG_RAW_RESPONSES = [
    "ws://192.168.0.1:7755/agent",
    "coordinator-api-key-2",
    "10 minutes",
    "3 seconds",
    "remote1",
    "2",
    "agent-key-2",
    "2",
    "2",
    "2",
    "tcp://192.168.0.1:2375",
    "1",
    "http://localhost:9999",
    "user1",
    "pass1",
    "2"
]
_CUSTOM_AND_SERVER_CONFIG_FORMATTED_RESPONSE_DICT: dict = {
    "coordinator_host": "ws://192.168.0.1:7755/agent",
    "coordinator_api_key": "coordinator-api-key-2",
    "coordinator_ping": "10 minutes",
    "coordinator_pong": "3 seconds",
    "identification_host_id": "remote1",
    "identification_type": "filesystem",
    "identification_agent_key": "agent-key-2",
    "logging_min_level": "info",
    "logging_json": "no",
    "docker_connection_type": "tcp",
    "docker_connection_uri": "tcp://192.168.0.1:2375",
    "docker_registry_configure_first": "yes",
    "docker_registry_host": "http://localhost:9999",
    "docker_registry_username": "user1",
    "docker_registry_password": "pass1",
    "result_rendering": "file"
}


class DockerAgentConfigWizardTest(unittest.TestCase):

    def setUp(self) -> None:
        self.wizard_result_transformer_mock: AbstractWizardResultTransformer = mock.create_autospec(AbstractWizardResultTransformer)
        self.wizard_result_console_renderer_mock: WizardResultConsoleRenderer = mock.create_autospec(WizardResultConsoleRenderer)
        self.wizard_result_file_renderer_mock: WizardResultFileRenderer = mock.create_autospec(WizardResultFileRenderer)

        self.wizard_result_transformer_mock.transform.return_value = _TRANSFORMED_VALUE

        self.docker_agent_config_wizard: DockerAgentConfigWizard = DockerAgentConfigWizard(
            self.wizard_result_transformer_mock,
            self.wizard_result_console_renderer_mock,
            self.wizard_result_file_renderer_mock)

    @mock.patch("builtins.input", side_effect=_DEFAULTS_NO_SERVER_RAW_RESPONSES)
    def test_should_run_wizard_for_configuration_with_defaults_and_no_server_and_console_rendering(self, _):

        # when
        self.docker_agent_config_wizard.run()

        # then
        self.wizard_result_transformer_mock.transform.assert_called_once_with(_DEFAULTS_NO_SERVER_FORMATTED_RESPONSE_DICT)
        self.wizard_result_console_renderer_mock.render.assert_called_once_with(_TRANSFORMED_VALUE)

    @mock.patch("builtins.input", side_effect=_CUSTOM_AND_SERVER_CONFIG_RAW_RESPONSES)
    def test_should_run_wizard_for_configuration_with_server_config_and_file_rendering(self, _):

        # when
        self.docker_agent_config_wizard.run()

        # then
        file_renderer_call_args = self.wizard_result_file_renderer_mock.render.call_args.args
        merge_lambda_result = file_renderer_call_args[1]({"domino": {"key": "value"}})

        self.wizard_result_transformer_mock.transform.assert_called_once_with(_CUSTOM_AND_SERVER_CONFIG_FORMATTED_RESPONSE_DICT)
        self.assertEqual(file_renderer_call_args[0], _TRANSFORMED_VALUE)
        self.assertEqual(merge_lambda_result, {"key": "value"})


if __name__ == "__main__":
    unittest.main()
