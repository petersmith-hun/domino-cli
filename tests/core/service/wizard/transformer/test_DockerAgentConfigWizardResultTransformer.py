import unittest

from domino_cli.core.service.wizard.transformer.DockerAgentConfigWizardResultTransformer import \
    DockerAgentConfigWizardResultTransformer

_DEFAULTS_NO_SERVER_RAW: dict = {
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
_DEFAULTS_NO_SERVER_TRANSFORMED: dict = {
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
                "type": "DOCKER",
                "agent-key": "agent-key-1"
            }
        },
        "logging": {
            "min-level": "warn",
            "enable-json-logging": True
        },
        "docker": {
            "connection": {
                "type": "socket",
                "uri": "/var/run/docker.sock"
            },
            "servers": []
        }
    }
}

_CUSTOM_AND_SERVER_CONFIG_RAW: dict = {
    "coordinator_host": "ws://192.168.0.1:7755/agent",
    "coordinator_api_key": "coordinator-api-key-2",
    "coordinator_ping": "10 minutes",
    "coordinator_pong": "3 seconds",
    "identification_host_id": "remote1",
    "identification_type": "docker",
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
_CUSTOM_AND_SERVER_CONFIG_TRANSFORMED: dict = {
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
                "type": "DOCKER",
                "agent-key": "agent-key-2"
            }
        },
        "logging": {
            "min-level": "info",
            "enable-json-logging": False
        },
        "docker": {
            "connection": {
                "type": "tcp",
                "uri": "tcp://192.168.0.1:2375"
            },
            "servers": [
                {
                    "host": "http://localhost:9999",
                    "username": "user1",
                    "password": "pass1"
                }
            ]
        }
    }
}


class DockerAgentConfigWizardResultTransformerTest(unittest.TestCase):

    def setUp(self) -> None:
        self.docker_agent_config_wizard_result_transformer: DockerAgentConfigWizardResultTransformer = DockerAgentConfigWizardResultTransformer()

    def test_should_transform(self):

        for (source, expected_target) in DockerAgentConfigWizardResultTransformerTest._prepare_parameters():
            with self.subTest("answer dictionary transformation", source=source, expected_target=expected_target):

                # when
                result: dict = self.docker_agent_config_wizard_result_transformer.transform(source)

                # then
                self.assertEqual(result, expected_target)

    @staticmethod
    def _prepare_parameters():
        return [
            (_DEFAULTS_NO_SERVER_RAW, _DEFAULTS_NO_SERVER_TRANSFORMED),
            (_CUSTOM_AND_SERVER_CONFIG_RAW, _CUSTOM_AND_SERVER_CONFIG_TRANSFORMED)
        ]


if __name__ == "__main__":
    unittest.main()
