from domino_cli.core.service.wizard.AbstractWizard import AbstractWizard
from domino_cli.core.service.wizard.installer.PlatformComponentInstaller import PlatformComponentInstaller
from domino_cli.core.service.wizard.mapping.InstallerWizardDataMapping import Mapping
from domino_cli.core.service.wizard.step.BaseWizardStep import BaseWizardStep
from domino_cli.core.service.wizard.step.OptionSelectorWizardStep import OptionSelectorWizardStep

_WIZARD_NAME = "installer"
_WIZARD_DESCRIPTION = "Installs Domino Platform components"
_AVAILABLE_COMPONENTS = ["coordinator", "docker-agent", "binary-executable-agent"]


class InstallerWizard(AbstractWizard):
    """
    AbstractWizard implementation for installing Domino Platform components.
    """
    def __init__(self,
                 docker_platform_component_installer: PlatformComponentInstaller,
                 bin_exec_platform_component_installer: PlatformComponentInstaller):
        super().__init__(_WIZARD_NAME, _WIZARD_DESCRIPTION)
        self._docker_platform_component_installer: PlatformComponentInstaller = docker_platform_component_installer
        self._bin_exec_platform_component_installer: PlatformComponentInstaller = bin_exec_platform_component_installer

    def _init_wizard(self) -> None:

        # steps
        ws_component_selector = OptionSelectorWizardStep(Mapping.COMPONENT, "Which Domino Platform component do you want to install?", _AVAILABLE_COMPONENTS)
        ws_container_name_coordinator = BaseWizardStep(Mapping.DOCKER_CONTAINER_NAME, "Specify name of the container", "domino_coordinator")
        ws_container_name_docker_agent = BaseWizardStep(Mapping.DOCKER_CONTAINER_NAME, "Specify name of the container", "domino_docker_agent")
        ws_config_filename_coordinator = BaseWizardStep(Mapping.CONFIGURATION_FILENAME, "Specify configuration filename without path and extension", "coordinator_production")
        ws_config_filename_docker_agent = BaseWizardStep(Mapping.CONFIGURATION_FILENAME, "Specify configuration filename without path and extension", "docker_agent_production")
        ws_config_filename_bin_exec_agent = BaseWizardStep(Mapping.CONFIGURATION_FILENAME, "Specify configuration filename without path and extension", "binary_executable_agent_production")
        ws_deployments_filename = BaseWizardStep(Mapping.DEPLOYMENTS_FILENAME, "Specify deployments configuration filename without path and extension", "deployments_production")
        ws_target_binary_location = BaseWizardStep(Mapping.TARGET_BINARY_LOCATION, "Specify binary target location on host (as absolute path)")
        ws_config_location = BaseWizardStep(Mapping.CONFIGURATION_FILE_LOCATION, "Specify configuration location on host (as absolute path)")
        ws_host_port = BaseWizardStep(Mapping.DOCKER_HOST_PORT, "Specify container port to expose to host", "9987")
        ws_network_mode = BaseWizardStep(Mapping.DOCKER_NETWORK_MODE, "Specify container network mode", "host")

        component_field = Mapping.COMPONENT.get_wizard_field()

        # transitions
        ws_component_selector.add_transition(ws_container_name_coordinator, lambda context: context[component_field] == "coordinator")
        ws_component_selector.add_transition(ws_container_name_docker_agent, lambda context: context[component_field] == "docker-agent")
        ws_component_selector.add_transition(ws_config_filename_bin_exec_agent, lambda context: context[component_field] == "binary-executable-agent")
        ws_container_name_coordinator.add_transition(ws_config_filename_coordinator)
        ws_container_name_docker_agent.add_transition(ws_config_filename_docker_agent)
        ws_config_filename_coordinator.add_transition(ws_deployments_filename)
        ws_config_filename_docker_agent.add_transition(ws_config_location)
        ws_config_filename_bin_exec_agent.add_transition(ws_target_binary_location)
        ws_target_binary_location.add_transition(ws_config_location)
        ws_deployments_filename.add_transition(ws_config_location)
        ws_config_location.add_transition(ws_host_port, lambda context: context[component_field] == "coordinator")
        ws_config_location.add_transition(ws_network_mode, lambda context: context[component_field] == "docker-agent")
        ws_host_port.add_transition(ws_network_mode)

        self.set_entry_point(ws_component_selector)

    def _handle_result(self, result: dict) -> None:

        if result[Mapping.COMPONENT.get_wizard_field()] in ["coordinator", "docker-agent"]:
            self._docker_platform_component_installer.install(result)
        else:
            self._bin_exec_platform_component_installer.install(result)
