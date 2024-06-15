from enum import Enum

from core.service.wizard.mapping.WizardDataMappingBaseEnum import WizardDataMappingBaseEnum, \
    _DEFAULT_OPTIONS_TO_BOOLEAN_MAPPER


class MappingGroups(Enum):
    BASE = "base"
    FIRST_SERVER = "first-server"

class Mapping(WizardDataMappingBaseEnum):
    """
    Field mappings between raw wizard response data and target data dictionaries.
    """
    COORDINATOR_HOST = (MappingGroups.BASE, "coordinator_host", "$root.agent.coordinator.host")
    COORDINATOR_API_KEY = (MappingGroups.BASE, "coordinator_api_key", "$root.agent.coordinator.api-key")
    COORDINATOR_PING = (MappingGroups.BASE, "coordinator_ping", "$root.agent.coordinator.ping-interval")
    COORDINATOR_PONG = (MappingGroups.BASE, "coordinator_pong", "$root.agent.coordinator.pong-timeout")

    IDENTIFICATION_HOST_ID = (MappingGroups.BASE, "identification_host_id", "$root.agent.identification.host-id")
    IDENTIFICATION_TYPE = (MappingGroups.BASE, "identification_type", "$root.agent.identification.type")
    IDENTIFICATION_AGENT_KEY = (MappingGroups.BASE, "identification_agent_key", "$root.agent.identification.agent-key")

    LOGGING_MIN_LEVEL = (MappingGroups.BASE, "logging_min_level", "$root.logging.min-level")
    LOGGING_JSON = (MappingGroups.BASE, "logging_json", "$root.logging.enable-json-logging", _DEFAULT_OPTIONS_TO_BOOLEAN_MAPPER)

    DOCKER_CONNECTION_TYPE = (MappingGroups.BASE, "docker_connection_type", "$root.docker.connection.type")
    DOCKER_CONNECTION_URI = (MappingGroups.BASE, "docker_connection_uri", "$root.docker.connection.uri")
    DOCKER_CONFIGURE_FIRST = ("", "docker_registry_configure_first", "$root.docker.servers")
    DOCKER_SERVER_HOST = (MappingGroups.FIRST_SERVER, "docker_registry_host", "host")
    DOCKER_SERVER_USERNAME = (MappingGroups.FIRST_SERVER, "docker_registry_username", "username")
    DOCKER_SERVER_PASSWORD = (MappingGroups.FIRST_SERVER, "docker_registry_password", "password")

    RESULT_RENDERING = ("", "result_rendering", None)
