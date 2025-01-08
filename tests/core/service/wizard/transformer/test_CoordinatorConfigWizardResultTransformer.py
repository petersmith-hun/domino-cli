import unittest

import bcrypt

from domino_cli.core.service.wizard.transformer.CoordinatorConfigWizardResultTransformer import \
    CoordinatorConfigWizardResultTransformer

_DIRECT_AUTH_NO_FIRST_AGENT_RAW: dict = {
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
_DIRECT_AUTH_NO_FIRST_AGENT_TRANSFORMED: dict = {
    "domino": {
        "server": {
            "context-path": "/api",
            "host": "127.0.0.1",
            "port": 9876
        },
        "datasource": {
            "sqlite-datafile-path": "/opt/dpc/data/database.sqlite",
            "enable-auto-import": True,
        },
        "logging": {
            "min-level": "warn",
            "enable-json-logging": True
        },
        "auth": {
            "auth-mode": "direct",
            "expiration": "2 hours",
            "jwt-private-key": "jwt-pvt-key-1",
            "username": "admin1",
            "password": ""
        },
        "agent": {
            "operation-timeout": "2 minutes",
            "api-key": "",
            "known-agents": []
        },
        "info": {
            "app-name": "Coordinator Test",
            "abbreviation": "DPC-TEST"
        }
    }
}

_OAUTH_AUTH_FIRST_AGENT_DEFAULTS_RAW: dict = {
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
_OAUTH_AUTH_FIRST_AGENT_DEFAULTS_TRANSFORMED: dict = {
    "domino": {
        "server": {
            "context-path": "/",
            "host": "0.0.0.0",
            "port": 9987
        },
        "datasource": {
            "sqlite-datafile-path": "./data/database.sqlite",
            "enable-auto-import": False,
        },
        "logging": {
            "min-level": "info",
            "enable-json-logging": False
        },
        "auth": {
            "auth-mode": "oauth",
            "oauth-issuer": "http://localhost:9999/",
            "oauth-audience": "dpc:test"
        },
        "agent": {
            "operation-timeout": "1 minute",
            "api-key": "",
            "known-agents": [
                {
                    "host-id": "devlocal",
                    "type": "DOCKER",
                    "agent-key": "agent-key-docker1"
                }
            ]
        },
        "info": {
            "app-name": "Coordinator Test 2",
            "abbreviation": "DPC-TEST2"
        }
    }
}


class CoordinatorConfigWizardResultTransformerTest(unittest.TestCase):

    def setUp(self) -> None:
        self.coordinator_config_wizard_result_transformer: CoordinatorConfigWizardResultTransformer = CoordinatorConfigWizardResultTransformer()

    def test_should_transform(self):

        for (source, expected_target) in CoordinatorConfigWizardResultTransformerTest._prepare_parameters():
            with self.subTest("answer dictionary transformation", source=source, expected_target=expected_target):

                # when
                result: dict = self.coordinator_config_wizard_result_transformer.transform(source)

                # then
                if "auth_password" in source:
                    self._verify_encrypted_value(source["auth_password"], result["domino"]["auth"]["password"])
                    result["domino"]["auth"]["password"] = ""
                self._verify_encrypted_value(source["agent_api_key"], result["domino"]["agent"]["api-key"])
                result["domino"]["agent"]["api-key"] = ""

                self.assertEqual(result, expected_target)

    @staticmethod
    def _prepare_parameters():
        return [
            (_DIRECT_AUTH_NO_FIRST_AGENT_RAW, _DIRECT_AUTH_NO_FIRST_AGENT_TRANSFORMED),
            (_OAUTH_AUTH_FIRST_AGENT_DEFAULTS_RAW, _OAUTH_AUTH_FIRST_AGENT_DEFAULTS_TRANSFORMED)
        ]

    def _verify_encrypted_value(self, source: str, result: str) -> None:
        self.assertTrue(bcrypt.checkpw(source.encode(), result.encode()))


if __name__ == "__main__":
    unittest.main()
