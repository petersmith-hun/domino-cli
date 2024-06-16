from enum import Enum

from core.service.wizard.mapping.WizardDataMappingBaseEnum import WizardDataMappingBaseEnum


class MappingGroups(Enum):
    BASE = "base"
    FIRST_SERVER = "first-server"


class Mapping(WizardDataMappingBaseEnum):
    """
    Field mappings between raw wizard response data and target data dictionaries for Docker Agent configuration.
    """
    DOCKER_CONNECTION_TYPE = (MappingGroups.BASE, "docker_connection_type", "$root.docker.connection.type")
    DOCKER_CONNECTION_URI = (MappingGroups.BASE, "docker_connection_uri", "$root.docker.connection.uri")
    DOCKER_CONFIGURE_FIRST = ("", "docker_registry_configure_first", "$root.docker.servers")
    DOCKER_SERVER_HOST = (MappingGroups.FIRST_SERVER, "docker_registry_host", "host")
    DOCKER_SERVER_USERNAME = (MappingGroups.FIRST_SERVER, "docker_registry_username", "username")
    DOCKER_SERVER_PASSWORD = (MappingGroups.FIRST_SERVER, "docker_registry_password", "password")
