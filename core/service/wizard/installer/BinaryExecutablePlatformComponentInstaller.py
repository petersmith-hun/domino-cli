from typing import List

from installer_config import installer_config
from core.service.wizard.installer import VersionResolver
from core.service.wizard.installer.PlatformComponentInstaller import PlatformComponentInstaller
from core.service.wizard.mapping.InstallerWizardDataMapping import Mapping
from installer_config import DominoComponent


_systemd_descriptor_template: str = """[Unit]
Description=Domino Platform Binary Executable Agent

[Service]
User=root
WorkingDirectory={workdir}
Environment=NODE_ENV={profile} NODE_CONFIG_DIR={confdir}
ExecStart={workdir}/{binary}
SuccessExitStatus=143
TimeoutStopSec=10
Restart=yes

[Install]
WantedBy=multi-user.target
"""


class BinaryExecutablePlatformComponentInstaller(PlatformComponentInstaller):
    """
    PlatformComponentInstaller implementation for binary executable based installations. Components of such will be
    installed as systemd services. Prepares the necessary Shell calls (wget for downloading the binary, chmod to add
    execution permission, mv to move the prepared service descriptor into the target folder, and systemctl calls to
    set up the service).
    """

    def __init__(self, version_resolver: VersionResolver):
        super().__init__(version_resolver)

    def _prepare_command_lines(self, component: DominoComponent, wizard_data: dict, version: str) -> List[List[str]]:

        target_binary_location = self._extract_value(wizard_data, Mapping.TARGET_BINARY_LOCATION)
        binary_name = installer_config.component_installed_name[component]
        target_binary_path = "{0}/{1}".format(target_binary_location, binary_name)
        source_url = self._replace_placeholders(installer_config.executable_source, component, wizard_data, version)
        resolved_systemd_descriptor = self._replace_placeholders(_systemd_descriptor_template, component, wizard_data, version)
        service_name = "{0}.service".format(binary_name)
        service_file_path_tmp = "/tmp/{0}.tmp".format(service_name)
        service_file_path_target = "/etc/systemd/system/{0}".format(service_name)

        with open(service_file_path_tmp, "w") as service_file:
            service_file.write(resolved_systemd_descriptor)

        download_command: List[str] = ["wget", "-O", target_binary_path, source_url]
        chmod_command: List[str] = ["chmod", "u+x", target_binary_path]
        service_creation_command: List[str] = ["mv", service_file_path_tmp, service_file_path_target]
        systemctl_reload_command = ["systemctl", "daemon-reload"]
        systemctl_enable_command = ["systemctl", "enable", service_name]
        systemctl_start_command = ["systemctl", "restart", service_name]

        return [
            download_command,
            chmod_command,
            service_creation_command,
            systemctl_reload_command,
            systemctl_enable_command,
            systemctl_start_command
        ]

    def _reported_installation_method(self) -> str:
        return "systemd service"

    def _replace_placeholders(self, source: str, component: DominoComponent, wizard_data: dict, version: str) -> str:

        return source \
            .replace("{component}", component.value) \
            .replace("{version}", version) \
            .replace("{workdir}", self._extract_value(wizard_data, Mapping.TARGET_BINARY_LOCATION)) \
            .replace("{confdir}", self._extract_value(wizard_data, Mapping.CONFIGURATION_FILE_LOCATION)) \
            .replace("{profile}", self._extract_value(wizard_data, Mapping.CONFIGURATION_FILENAME)) \
            .replace("{binary}", installer_config.component_installed_name[component])
