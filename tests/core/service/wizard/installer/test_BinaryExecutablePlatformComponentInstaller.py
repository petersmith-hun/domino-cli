import unittest
from unittest import mock
from unittest.mock import mock_open

from domino_cli.core.service.wizard.installer import VersionResolver
from domino_cli.core.service.wizard.installer.BinaryExecutablePlatformComponentInstaller import \
    BinaryExecutablePlatformComponentInstaller


_INSTALL_BIN_EXEC_AGENT_RESPONSE_DICT: dict = {
    "component": "binary-executable-agent",
    "configuration_filename": "binary_executable_agent_test",
    "target_binary_location": "/opt/agent",
    "config_location": "/opt/config"
}
_EXPECTED_SERVICE_DESCRIPTOR = """[Unit]
Description=Domino Platform Binary Executable Agent

[Service]
User=root
WorkingDirectory=/opt/agent
Environment=NODE_ENV=binary_executable_agent_test NODE_CONFIG_DIR=/opt/config
ExecStart=/opt/agent/domino-bin-exec-agent
SuccessExitStatus=143
TimeoutStopSec=10
Restart=yes

[Install]
WantedBy=multi-user.target
"""


class BinaryExecutablePlatformComponentInstallerTest(unittest.TestCase):

    def setUp(self):
        self.version_resolver_mock: VersionResolver = mock.create_autospec(VersionResolver)
        self.bin_exec_platform_component_installer = \
            BinaryExecutablePlatformComponentInstaller(self.version_resolver_mock)

    @mock.patch("builtins.input", return_value="yes")
    @mock.patch("builtins.open", new_callable=mock_open)
    @mock.patch("subprocess.call")
    def test_should_install_bin_exec_agent(self, subprocess_call_mock, open_mock, input_mock):

        # given
        self.version_resolver_mock.resolve_latest.return_value = "1.2.0-1"

        # when
        self.bin_exec_platform_component_installer.install(_INSTALL_BIN_EXEC_AGENT_RESPONSE_DICT)

        # then
        service_descriptor_contents = open_mock.return_value.write.call_args.args[0]
        self.assertEqual(service_descriptor_contents, _EXPECTED_SERVICE_DESCRIPTOR)

        input_mock.assert_called_once()

        self.assertEqual(subprocess_call_mock.call_count, 6)
        subprocess_call_mock.assert_has_calls([
            mock.call(["wget", "-O", "/opt/agent/domino-bin-exec-agent", "https://github.com/petersmith-hun/domino-platform/releases/download/binary-executable-agent-linux-x64-v1.2.0-1-release/domino-binary-executable-agent"]),
            mock.call(["chmod", "u+x", "/opt/agent/domino-bin-exec-agent"]),
            mock.call(["mv", "/tmp/domino-bin-exec-agent.service.tmp", "/etc/systemd/system/domino-bin-exec-agent.service"]),
            mock.call(["systemctl", "daemon-reload"]),
            mock.call(["systemctl", "enable", "domino-bin-exec-agent.service"]),
            mock.call(["systemctl", "restart", "domino-bin-exec-agent.service"])
        ])

    @mock.patch("builtins.input", return_value="no")
    @mock.patch("builtins.open", new_callable=mock_open)
    @mock.patch("subprocess.call")
    def test_should_not_install_bin_exec_agent_when_rejected(self, subprocess_call_mock, open_mock, input_mock):

        # given
        self.version_resolver_mock.resolve_latest.return_value = "1.2.0-1"

        # when
        self.bin_exec_platform_component_installer.install(_INSTALL_BIN_EXEC_AGENT_RESPONSE_DICT)

        # then
        open_mock.assert_called_once()
        input_mock.assert_called_once()
        subprocess_call_mock.assert_not_called()


if __name__ == "__main__":
    unittest.main()
