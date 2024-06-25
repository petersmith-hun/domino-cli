from typing import List

from core.service.wizard.installer import VersionResolver
from core.service.wizard.installer.PlatformComponentInstaller import PlatformComponentInstaller
from core.service.wizard.mapping.InstallerWizardDataMapping import Mapping, MappingGroups
from installer_config import DominoComponent, installer_config


class DockerPlatformComponentInstaller(PlatformComponentInstaller):
    """
    PlatformComponentInstaller implementation for Docker based installations. Prepares the necessary Docker CLI calls
    (docker rm ... for clean-up, docker run ... for installation).
    """
    def __init__(self, version_resolver: VersionResolver):
        super().__init__(version_resolver)

    def _prepare_command_lines(self, component: DominoComponent, wizard_data: dict, version: str) -> List[List[str]]:

        docker_remove_command: List[str] = [
            "docker",
            "rm",
            "-f",
            wizard_data[Mapping.DOCKER_CONTAINER_NAME.get_wizard_field()]
        ]

        docker_run_command: List[str] = [
            "docker",
            "run",
            "--detach",
            "--restart", "unless-stopped",
            *self._create_environment_variables(component, wizard_data),
            *self._create_volume_directive(component, wizard_data),
            *self._create_port_exposure(component, wizard_data)
        ]

        for mapping in Mapping.get_mappings_by_group(MappingGroups.COMMON):
            for arg in self._extract_value(wizard_data, mapping).split(" "):
                docker_run_command.append(arg)

        image = ("{0}/{1}:{2}".format(installer_config.docker_registry,
                                      installer_config.component_installed_name[component], version))

        docker_run_command.append(image)

        return [docker_remove_command, docker_run_command]

    def _reported_installation_method(self) -> str:
        return "Docker container"

    def _create_environment_variables(self, component: DominoComponent, wizard_data: dict) -> List[str]:

        return [
            "-e", self._create_profile_directive(component, wizard_data),
            "-e", "NODE_CONF_DIR=/opt/{0}/config".format(component.value),
            "-e", "NODE_OPTIONS=--max_old_space_size={0}".format(installer_config.docker_container_heap_size[component]),
        ]

    def _create_profile_directive(self, component: DominoComponent, wizard_data: dict) -> str:

        environment = self._extract_value(wizard_data, Mapping.CONFIGURATION_FILENAME)
        if self._is_coordinator(component):
            deployment_environment = self._extract_value(wizard_data, Mapping.DEPLOYMENTS_FILENAME)
            environment = "{0},{1}".format(environment, deployment_environment)

        return "NODE_ENV={0}".format(environment)

    def _create_volume_directive(self, component: DominoComponent, wizard_data: dict) -> List[str]:

        config_volume = self._extract_value(wizard_data, Mapping.CONFIGURATION_FILE_LOCATION)
        volumes: List[str] = ["-v", "{0}:/opt/{1}/config:ro".format(config_volume, component.value)]

        if not self._is_coordinator(component):
            volumes = volumes + ["-v", "/var/run/docker.sock:/var/run/docker.sock"]

        return volumes

    def _create_port_exposure(self, component: DominoComponent, wizard_data: dict) -> List[str]:

        return self._extract_value(wizard_data, Mapping.DOCKER_HOST_PORT).split(" ") \
            if self._is_coordinator(component) \
            else []

    @staticmethod
    def _is_coordinator(component: DominoComponent) -> bool:
        return component == DominoComponent.COORDINATOR
