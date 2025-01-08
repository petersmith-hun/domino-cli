from enum import Enum

from domino_cli.core.service.wizard.mapping.WizardDataMappingBaseEnum import WizardDataMappingBaseEnum, \
    _DEFAULT_OPTIONS_TO_BOOLEAN_MAPPER
from domino_cli.installer_config import DominoComponent


class MappingGroups(Enum):
    COMMON = "common"
    CONFIGURATION = "configuration"
    COORDINATOR_ONLY = "coordinator-only"


class Mapping(WizardDataMappingBaseEnum):
    """
    Field mappings between raw wizard response data and target data dictionaries for installer.
    """
    COMPONENT = ("", "component", "", lambda value: DominoComponent(value))

    DOCKER_CONTAINER_NAME = (MappingGroups.COMMON, "container_name", "", lambda value: "--name {0}".format(value))
    DOCKER_NETWORK_MODE = (MappingGroups.COMMON, "network_mode", "", lambda value: "--network {0}".format(value))

    DOCKER_HOST_PORT = (MappingGroups.COORDINATOR_ONLY, "host_port", "", lambda value: "-p {0}:9987".format(value))

    CONFIGURATION_FILENAME = (MappingGroups.CONFIGURATION, "configuration_filename", "")
    ENABLE_DEPLOYMENTS_FILE = (MappingGroups.CONFIGURATION, "enable_deployments_file", "", _DEFAULT_OPTIONS_TO_BOOLEAN_MAPPER)
    DEPLOYMENTS_FILENAME = (MappingGroups.CONFIGURATION, "deployments_filename", "")
    CONFIGURATION_FILE_LOCATION = (MappingGroups.CONFIGURATION, "config_location", "")
    SQLITE_DATAFILE_LOCATION = (MappingGroups.CONFIGURATION, "sqlite_location", "")
    TARGET_BINARY_LOCATION = (MappingGroups.CONFIGURATION, "target_binary_location", "")
