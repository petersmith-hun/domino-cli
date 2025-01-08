from enum import Enum

from domino_cli.core.service.wizard.mapping.WizardDataMappingBaseEnum import WizardDataMappingBaseEnum, \
    _DEFAULT_OPTIONS_TO_BOOLEAN_MAPPER, _UPPERCASE_MAPPER


class CommonMappingGroups(Enum):
    BASE = "base"


class CommonMapping(WizardDataMappingBaseEnum):
    """
    Field mappings between raw wizard response data and target data dictionaries.
    """
    COORDINATOR_HOST = (CommonMappingGroups.BASE, "coordinator_host", "$root.agent.coordinator.host")
    COORDINATOR_API_KEY = (CommonMappingGroups.BASE, "coordinator_api_key", "$root.agent.coordinator.api-key")
    COORDINATOR_PING = (CommonMappingGroups.BASE, "coordinator_ping", "$root.agent.coordinator.ping-interval")
    COORDINATOR_PONG = (CommonMappingGroups.BASE, "coordinator_pong", "$root.agent.coordinator.pong-timeout")

    IDENTIFICATION_HOST_ID = (CommonMappingGroups.BASE, "identification_host_id", "$root.agent.identification.host-id")
    IDENTIFICATION_TYPE = (CommonMappingGroups.BASE, "identification_type", "$root.agent.identification.type", _UPPERCASE_MAPPER)
    IDENTIFICATION_AGENT_KEY = (CommonMappingGroups.BASE, "identification_agent_key", "$root.agent.identification.agent-key")

    LOGGING_MIN_LEVEL = (CommonMappingGroups.BASE, "logging_min_level", "$root.logging.min-level")
    LOGGING_JSON = (CommonMappingGroups.BASE, "logging_json", "$root.logging.enable-json-logging", _DEFAULT_OPTIONS_TO_BOOLEAN_MAPPER)

    RESULT_RENDERING = ("", "result_rendering", None)
