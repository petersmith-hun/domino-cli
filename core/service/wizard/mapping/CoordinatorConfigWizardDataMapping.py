from enum import Enum

from core.service.wizard.mapping.WizardDataMappingBaseEnum import WizardDataMappingBaseEnum, \
    _DEFAULT_OPTIONS_TO_BOOLEAN_MAPPER, _STR_TO_INT_MAPPER, _BCRYPT_MAPPER


class MappingGroups(Enum):
    BASE = "base"
    JWT = "jwt"
    OAUTH = "oauth"
    FIRST_AGENT = "first-agent"


class Mapping(WizardDataMappingBaseEnum):
    """
    Field mappings between raw wizard response data and target data dictionaries.
    """
    SERVER_CONTEXT_PATH = (MappingGroups.BASE, "server_context_path", "$root.server.context-path")
    SERVER_HOST = (MappingGroups.BASE, "server_host", "$root.server.host")
    SERVER_PORT = (MappingGroups.BASE, "server_port", "$root.server.port", _STR_TO_INT_MAPPER)

    LOGGING_MIN_LEVEL = (MappingGroups.BASE, "logging_min_level", "$root.logging.min-level")
    LOGGING_JSON = (MappingGroups.BASE, "logging_json", "$root.logging.enable-json-logging", _DEFAULT_OPTIONS_TO_BOOLEAN_MAPPER)

    AUTH_MODE = (MappingGroups.BASE, "auth_mode", "$root.auth.auth-mode")
    AUTH_EXPIRATION = (MappingGroups.JWT, "auth_expiration", "$root.auth.expiration")
    AUTH_JWT_PRIVATE_KEY = (MappingGroups.JWT, "auth_jwt_private_key", "$root.auth.jwt-private-key")
    AUTH_USERNAME = (MappingGroups.JWT, "auth_username", "$root.auth.username")
    AUTH_PASSWORD = (MappingGroups.JWT, "auth_password", "$root.auth.password", _BCRYPT_MAPPER)
    AUTH_OAUTH_ISSUER = (MappingGroups.OAUTH, "auth_oauth_issuer", "$root.auth.oauth-issuer")
    AUTH_OAUTH_AUDIENCE = (MappingGroups.OAUTH, "auth_oauth_audience", "$root.auth.oauth-audience")

    AGENT_OPERATION_TIMEOUT = (MappingGroups.BASE, "agent_operation_timeout", "$root.agent.operation-timeout")
    AGENT_API_KEY = (MappingGroups.BASE, "agent_api_key", "$root.agent.api-key", _BCRYPT_MAPPER)
    AGENT_CONFIGURE_FIRST = ("", "agent_configure_first", "$root.agent.known-agents")
    AGENT_HOST_ID = (MappingGroups.FIRST_AGENT, "agent_host_id", "host-id")
    AGENT_TYPE = (MappingGroups.FIRST_AGENT, "agent_type", "type")
    AGENT_AGENT_KEY = (MappingGroups.FIRST_AGENT, "agent_key", "agent-key")

    INFO_APP_NAME = (MappingGroups.BASE, "info_app_name", "$root.info.app-name")
    INFO_ABBREVIATION = (MappingGroups.BASE, "info_abbreviation", "$root.info.abbreviation")

    RESULT_RENDERING = ("", "result_rendering", None)
