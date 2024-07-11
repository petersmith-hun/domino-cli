import unittest

from domino_cli.core.service.wizard.transformer.BinaryExecutableAgentConfigWizardResultTransformer import \
    BinaryExecutableAgentConfigWizardResultTransformer

_DEFAULTS_NO_RUNTIME_RAW: dict = {
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
_DEFAULTS_NO_RUNTIME_TRANSFORMED: dict = {
    "domino": {
        "agent": {
            "coordinator": {
                "host": "ws://127.0.0.1:9987/agent",
                "api-key": "coordinator-api-key",
                "ping-interval": "5 minutes",
                "pong-timeout": "2 seconds"
            },
            "identification": {
                "host-id": "devlocal",
                "type": "docker",
                "agent-key": "agent-key-1"
            }
        },
        "logging": {
            "min-level": "warn",
            "enable-json-logging": True
        },
        "spawn-control": {
            "service-handler": "systemd",
            "start-delay": "3 seconds",
            "allowed-executor-users": [
                "leaflet",
                "domino"
            ]
        },
        "storage": {
            "deployment-store-path": "./storage/deployments",
            "application-home-path": "./storage/home"
        }
    }
}

_CUSTOM_AND_RUNTIME_CONFIG_RAW: dict = {
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
_CUSTOM_AND_RUNTIME_CONFIG_TRANSFORMED: dict = {
    "domino": {
        "agent": {
            "coordinator": {
                "host": "ws://192.168.0.1:7755/agent",
                "api-key": "coordinator-api-key-2",
                "ping-interval": "10 minutes",
                "pong-timeout": "3 seconds"
            },
            "identification": {
                "host-id": "remote1",
                "type": "filesystem",
                "agent-key": "agent-key-2"
            }
        },
        "logging": {
            "min-level": "info",
            "enable-json-logging": False
        },
        "spawn-control": {
            "service-handler": "systemd",
            "start-delay": "5 seconds",
            "allowed-executor-users": [
                "leaflet"
            ]
        },
        "storage": {
            "deployment-store-path": "/opt/storage/deployments",
            "application-home-path": "/opt/storage/home"
        },
        "runtimes": [
            {
                "id": "java",
                "binary-path": "/bin/java",
                "healthcheck": "--version",
                "command-line": "{args} -jar {resource}"
            }
        ]
    }
}


class BinaryExecutableAgentConfigWizardResultTransformerTest(unittest.TestCase):

    def setUp(self) -> None:
        self.binary_executable_agent_config_wizard_result_transformer: BinaryExecutableAgentConfigWizardResultTransformer = BinaryExecutableAgentConfigWizardResultTransformer()

    def test_should_transform(self):

        for (source, expected_target) in BinaryExecutableAgentConfigWizardResultTransformerTest._prepare_parameters():
            with self.subTest("answer dictionary transformation", source=source, expected_target=expected_target):

                # when
                result: dict = self.binary_executable_agent_config_wizard_result_transformer.transform(source)

                # then
                self.assertEqual(result, expected_target)

    @staticmethod
    def _prepare_parameters():
        return [
            (_DEFAULTS_NO_RUNTIME_RAW, _DEFAULTS_NO_RUNTIME_TRANSFORMED),
            (_CUSTOM_AND_RUNTIME_CONFIG_RAW, _CUSTOM_AND_RUNTIME_CONFIG_TRANSFORMED)
        ]


if __name__ == "__main__":
    unittest.main()
