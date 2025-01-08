import unittest
from unittest import mock

from domino_cli.core.service.wizard.CoordinatorConfigWizard import CoordinatorConfigWizard
from domino_cli.core.service.wizard.render.WizardResultConsoleRenderer import WizardResultConsoleRenderer
from domino_cli.core.service.wizard.render.WizardResultFileRenderer import WizardResultFileRenderer
from domino_cli.core.service.wizard.transformer.AbstractWizardResultTransformer import AbstractWizardResultTransformer

_TRANSFORMED_VALUE = {"transformed": {}}

_DIRECT_AUTH_NO_FIRST_AGENT_RAW_RESPONSES = [
    "/api",
    "127.0.0.1",
    "9876",
    "/opt/dpc/data/database.sqlite",
    "1",
    "3",
    "1",
    "1",
    "2 hours",
    "jwt-pvt-key-1",
    "admin1",
    "pass1234",
    "2 minutes",
    "api-key-1",
    "2",
    "Coordinator Test",
    "DPC-TEST",
    "1"
]
_DIRECT_AUTH_NO_FIRST_AGENT_FORMATTED_RESPONSE_DICT: dict = {
    "server_context_path": "/api", 
    "server_host": "127.0.0.1",
    "server_port": "9876",
    "datasource_sqlite_datafile_path": "/opt/dpc/data/database.sqlite",
    "datasource_enable_auto_import": "yes",
    "logging_min_level": "warn",
    "logging_json": "yes", 
    "auth_mode": "direct",
    "auth_expiration": "2 hours",
    "auth_jwt_private_key": "jwt-pvt-key-1",
    "auth_username": "admin1",
    "auth_password": "pass1234",
    "agent_operation_timeout": "2 minutes",
    "agent_api_key": "api-key-1",
    "agent_configure_first": "no",
    "info_app_name": "Coordinator Test",
    "info_abbreviation": "DPC-TEST",
    "result_rendering": "console"
}

_OAUTH_AUTH_FIRST_AGENT_RAW_RESPONSES = [
    "",
    "",
    "",
    "",
    "2",
    "2",
    "2",
    "2",
    "http://localhost:9999/",
    "dpc:test",
    "1 minute",
    "api-key-2",
    "1",
    "devlocal",
    "1",
    "agent-key-docker1",
    "Coordinator Test 2",
    "DPC-TEST2",
    "2"
]
_OAUTH_AUTH_FIRST_AGENT_FORMATTED_RESPONSE_DICT: dict = {
    "server_context_path": "/",
    "server_host": "0.0.0.0",
    "server_port": "9987",
    "datasource_sqlite_datafile_path": "./data/database.sqlite",
    "datasource_enable_auto_import": "no",
    "logging_min_level": "info",
    "logging_json": "no",
    "auth_mode": "oauth",
    "auth_oauth_issuer": "http://localhost:9999/",
    "auth_oauth_audience": "dpc:test",
    "agent_operation_timeout": "1 minute",
    "agent_api_key": "api-key-2",
    "agent_configure_first": "yes",
    "agent_host_id": "devlocal",
    "agent_type": "docker",
    "agent_key": "agent-key-docker1",
    "info_app_name": "Coordinator Test 2",
    "info_abbreviation": "DPC-TEST2",
    "result_rendering": "file"
}


class CoordinatorConfigWizardTest(unittest.TestCase):

    def setUp(self) -> None:
        self.wizard_result_transformer_mock: AbstractWizardResultTransformer = mock.create_autospec(AbstractWizardResultTransformer)
        self.wizard_result_console_renderer_mock: WizardResultConsoleRenderer = mock.create_autospec(WizardResultConsoleRenderer)
        self.wizard_result_file_renderer_mock: WizardResultFileRenderer = mock.create_autospec(WizardResultFileRenderer)

        self.wizard_result_transformer_mock.transform.return_value = _TRANSFORMED_VALUE

        self.coordinator_config_wizard: CoordinatorConfigWizard = CoordinatorConfigWizard(
            self.wizard_result_transformer_mock,
            self.wizard_result_console_renderer_mock,
            self.wizard_result_file_renderer_mock)

    @mock.patch("builtins.input", side_effect=_DIRECT_AUTH_NO_FIRST_AGENT_RAW_RESPONSES)
    def test_should_run_wizard_for_configuration_with_direct_auth_and_no_first_agent_and_console_rendering(self, _):

        # when
        self.coordinator_config_wizard.run()

        # then
        self.wizard_result_transformer_mock.transform.assert_called_once_with(_DIRECT_AUTH_NO_FIRST_AGENT_FORMATTED_RESPONSE_DICT)
        self.wizard_result_console_renderer_mock.render.assert_called_once_with(_TRANSFORMED_VALUE)

    @mock.patch("builtins.input", side_effect=_OAUTH_AUTH_FIRST_AGENT_RAW_RESPONSES)
    def test_should_run_wizard_for_configuration_with_oauth_auth_and_with_agent_and_defaults_and_file_rendering(self, _):

        # when
        self.coordinator_config_wizard.run()

        # then
        file_renderer_call_args = self.wizard_result_file_renderer_mock.render.call_args.args
        merge_lambda_result = file_renderer_call_args[1]({"domino": {"key": "value"}})

        self.wizard_result_transformer_mock.transform.assert_called_once_with(_OAUTH_AUTH_FIRST_AGENT_FORMATTED_RESPONSE_DICT)
        self.assertEqual(file_renderer_call_args[0], _TRANSFORMED_VALUE)
        self.assertEqual(merge_lambda_result, {"key": "value"})


if __name__ == "__main__":
    unittest.main()
