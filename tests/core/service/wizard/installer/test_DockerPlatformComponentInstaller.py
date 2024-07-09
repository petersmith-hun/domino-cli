import unittest
from unittest import mock

from domino_cli.core.service.wizard.installer import VersionResolver
from domino_cli.core.service.wizard.installer.DockerPlatformComponentInstaller import DockerPlatformComponentInstaller


_INSTALL_COORDINATOR_RESPONSE_DICT: dict = {
    "component": "coordinator",
    "container_name": "domino_coordinator",
    "configuration_filename": "coordinator_production",
    "deployments_filename": "deployments_production",
    "config_location": "/opt/config",
    "host_port": "9987",
    "network_mode": "host"
}
_INSTALL_DOCKER_AGENT_RESPONSE_DICT: dict = {
    "component": "docker-agent",
    "container_name": "domino_docker_agent",
    "configuration_filename": "docker_agent_production",
    "config_location": "/opt/config",
    "network_mode": "host"
}


class DockerPlatformComponentInstallerTest(unittest.TestCase):

    def setUp(self):
        self.version_resolver_mock: VersionResolver = mock.create_autospec(VersionResolver)
        self.docker_platform_component_installer = \
            DockerPlatformComponentInstaller(self.version_resolver_mock)

    @mock.patch("builtins.input", return_value="yes")
    @mock.patch("subprocess.call")
    def test_should_install_coordinator(self, subprocess_call_mock, input_mock):

        # given
        self.version_resolver_mock.resolve_latest.return_value = "2.0.0-1"

        # when
        self.docker_platform_component_installer.install(_INSTALL_COORDINATOR_RESPONSE_DICT)

        # then
        input_mock.assert_called_once()
        self.assertEqual(subprocess_call_mock.call_count, 2)
        subprocess_call_mock.assert_has_calls([
            mock.call(['docker', 'rm', '-f', 'domino_coordinator']),
            mock.call(['docker', 'run',
                       '--detach',
                       '--restart', 'unless-stopped',
                       '-e', 'NODE_ENV=coordinator_production,deployments_production',
                       '-e', 'NODE_CONF_DIR=/opt/coordinator/config',
                       '-e', 'NODE_OPTIONS=--max_old_space_size=128',
                       '-v', '/opt/config:/opt/coordinator/config:ro',
                       '-p', '9987:9987',
                       '--name', 'domino_coordinator',
                       '--network', 'host',
                       'docker.io/psproghu/domino-coordinator:2.0.0-1'
            ])
        ])

    @mock.patch("builtins.input", return_value="yes")
    @mock.patch("subprocess.call")
    def test_should_install_docker_agent(self, subprocess_call_mock, input_mock):

        # given
        self.version_resolver_mock.resolve_latest.return_value = "1.1.0-5"

        # when
        self.docker_platform_component_installer.install(_INSTALL_DOCKER_AGENT_RESPONSE_DICT)

        # then
        input_mock.assert_called_once()
        self.assertEqual(subprocess_call_mock.call_count, 2)
        subprocess_call_mock.assert_has_calls([
            mock.call(['docker', 'rm', '-f', 'domino_docker_agent']),
            mock.call(['docker', 'run',
                       '--detach',
                       '--restart', 'unless-stopped',
                       '-e', 'NODE_ENV=docker_agent_production',
                       '-e', 'NODE_CONF_DIR=/opt/docker-agent/config',
                       '-e', 'NODE_OPTIONS=--max_old_space_size=64',
                       '-v', '/opt/config:/opt/docker-agent/config:ro',
                       '-v', '/var/run/docker.sock:/var/run/docker.sock',
                       '--name', 'domino_docker_agent',
                       '--network', 'host',
                       'docker.io/psproghu/domino-docker-agent:1.1.0-5'
            ])
        ])

    @mock.patch("builtins.input", return_value="no")
    @mock.patch("subprocess.call")
    def test_should_not_install_docker_agent_when_rejected(self, subprocess_call_mock, input_mock):

        # given
        self.version_resolver_mock.resolve_latest.return_value = "2.0.0-1"

        # when
        self.docker_platform_component_installer.install(_INSTALL_DOCKER_AGENT_RESPONSE_DICT)

        # then
        input_mock.assert_called_once()
        subprocess_call_mock.assert_not_called()


if __name__ == "__main__":
    unittest.main()
