import unittest
from unittest import mock

from domino_cli.core.service.wizard.InstallerWizard import InstallerWizard
from domino_cli.core.service.wizard.installer.PlatformComponentInstaller import PlatformComponentInstaller

_INSTALL_COORDINATOR_DEFAULTS_RAW_RESPONSES = [
    "1",
    "",
    "",
    "1",
    "",
    "/opt/config",
    "/opt/data",
    "",
    ""
]
_INSTALL_COORDINATOR_DEFAULTS_RESPONSE_DICT: dict = {
    "component": "coordinator",
    "container_name": "domino_coordinator",
    "configuration_filename": "coordinator_production",
    "enable_deployments_file": "yes",
    "deployments_filename": "deployments_production",
    "config_location": "/opt/config",
    "sqlite_location": "/opt/data",
    "host_port": "9987",
    "network_mode": "host"
}
_INSTALL_COORDINATOR_OVERRIDES_RAW_RESPONSES_NO_DEPLOYMENTS_FILE = [
    "1",
    "test-coordinator",
    "coordinator_test",
    "2",
    "/opt/config/test",
    "/opt/dpc/data",
    "1234",
    "bridge"
]
_INSTALL_COORDINATOR_OVERRIDES_RESPONSE_DICT_NO_DEPLOYMENTS_FILE: dict = {
    "component": "coordinator",
    "container_name": "test-coordinator",
    "configuration_filename": "coordinator_test",
    "enable_deployments_file": "no",
    "config_location": "/opt/config/test",
    "sqlite_location": "/opt/dpc/data",
    "host_port": "1234",
    "network_mode": "bridge"
}

_INSTALL_DOCKER_AGENT_DEFAULTS_RAW_RESPONSES = [
    "2",
    "",
    "",
    "/opt/config",
    ""
]
_INSTALL_DOCKER_AGENT_DEFAULTS_RESPONSE_DICT: dict = {
    "component": "docker-agent",
    "container_name": "domino_docker_agent",
    "configuration_filename": "docker_agent_production",
    "config_location": "/opt/config",
    "network_mode": "host"
}
_INSTALL_DOCKER_AGENT_OVERRIDES_RAW_RESPONSES = [
    "2",
    "test-docker-agent",
    "docker_agent_test",
    "/opt/config/test",
    "bridge"
]
_INSTALL_DOCKER_AGENT_OVERRIDES_RESPONSE_DICT: dict = {
    "component": "docker-agent",
    "container_name": "test-docker-agent",
    "configuration_filename": "docker_agent_test",
    "config_location": "/opt/config/test",
    "network_mode": "bridge"
}

_INSTALL_BIN_EXEC_AGENT_DEFAULTS_RAW_RESPONSES = [
    "3",
    "",
    "/opt/agent",
    "/opt/config"
]
_INSTALL_BIN_EXEC_AGENT_DEFAULTS_RESPONSE_DICT: dict = {
    "component": "binary-executable-agent",
    "configuration_filename": "binary_executable_agent_production",
    "target_binary_location": "/opt/agent",
    "config_location": "/opt/config"
}
_INSTALL_BIN_EXEC_AGENT_OVERRIDES_RAW_RESPONSES = [
    "3",
    "binary_executable_agent_test",
    "/opt/agent/test",
    "/opt/config/test"
]
_INSTALL_BIN_EXEC_AGENT_OVERRIDES_RESPONSE_DICT: dict = {
    "component": "binary-executable-agent",
    "configuration_filename": "binary_executable_agent_test",
    "target_binary_location": "/opt/agent/test",
    "config_location": "/opt/config/test"
}


class InstallerWizardTest(unittest.TestCase):

    def setUp(self) -> None:
        self.docker_platform_component_installer_mock: PlatformComponentInstaller = mock.create_autospec(PlatformComponentInstaller)
        self.bin_exec_platform_component_installer_mock: PlatformComponentInstaller = mock.create_autospec(PlatformComponentInstaller)

        self.installer_wizard: InstallerWizard = InstallerWizard(
            self.docker_platform_component_installer_mock,
            self.bin_exec_platform_component_installer_mock)

    @mock.patch("builtins.input", side_effect=_INSTALL_COORDINATOR_DEFAULTS_RAW_RESPONSES)
    def test_should_run_wizard_install_coordinator_with_defaults(self, _):

        # when
        self.installer_wizard.run()

        # then
        self.docker_platform_component_installer_mock.install.assert_called_once_with(_INSTALL_COORDINATOR_DEFAULTS_RESPONSE_DICT)

    @mock.patch("builtins.input", side_effect=_INSTALL_COORDINATOR_OVERRIDES_RAW_RESPONSES_NO_DEPLOYMENTS_FILE)
    def test_should_run_wizard_install_coordinator_with_overrides_no_deployments_file(self, _):

        # when
        self.installer_wizard.run()

        # then
        self.docker_platform_component_installer_mock.install.assert_called_once_with(_INSTALL_COORDINATOR_OVERRIDES_RESPONSE_DICT_NO_DEPLOYMENTS_FILE)

    @mock.patch("builtins.input", side_effect=_INSTALL_DOCKER_AGENT_DEFAULTS_RAW_RESPONSES)
    def test_should_run_wizard_install_docker_agent_with_defaults(self, _):

        # when
        self.installer_wizard.run()

        # then
        self.docker_platform_component_installer_mock.install.assert_called_once_with(_INSTALL_DOCKER_AGENT_DEFAULTS_RESPONSE_DICT)

    @mock.patch("builtins.input", side_effect=_INSTALL_DOCKER_AGENT_OVERRIDES_RAW_RESPONSES)
    def test_should_run_wizard_install_docker_agent_with_overrides(self, _):

        # when
        self.installer_wizard.run()

        # then
        self.docker_platform_component_installer_mock.install.assert_called_once_with(_INSTALL_DOCKER_AGENT_OVERRIDES_RESPONSE_DICT)

    @mock.patch("builtins.input", side_effect=_INSTALL_BIN_EXEC_AGENT_DEFAULTS_RAW_RESPONSES)
    def test_should_run_wizard_install_bin_exec_agent_with_defaults(self, _):

        # when
        self.installer_wizard.run()

        # then
        self.bin_exec_platform_component_installer_mock.install.assert_called_once_with(_INSTALL_BIN_EXEC_AGENT_DEFAULTS_RESPONSE_DICT)

    @mock.patch("builtins.input", side_effect=_INSTALL_BIN_EXEC_AGENT_OVERRIDES_RAW_RESPONSES)
    def test_should_run_wizard_install_bin_exec_agent_with_overrides(self, _):

        # when
        self.installer_wizard.run()

        # then
        self.bin_exec_platform_component_installer_mock.install.assert_called_once_with(_INSTALL_BIN_EXEC_AGENT_OVERRIDES_RESPONSE_DICT)


if __name__ == "__main__":
    unittest.main()
