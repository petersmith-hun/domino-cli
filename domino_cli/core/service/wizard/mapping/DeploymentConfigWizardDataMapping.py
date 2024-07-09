from enum import Enum

from domino_cli.core.service.wizard.mapping.WizardDataMappingBaseEnum import WizardDataMappingBaseEnum, _UPPERCASE_MAPPER, \
    _DEFAULT_OPTIONS_TO_BOOLEAN_MAPPER, _STR_TO_INT_MAPPER


class MappingGroups(Enum):
    BASE = "base"
    DOCKER_EXEC_ARGS = "docker-exec-args"
    HEALTH_CHECK = "healthcheck"
    INFO = "info"
    SOURCE_COMMON = "source-common"


class Mapping(WizardDataMappingBaseEnum):
    """
    Field mappings between raw wizard response data and target data dictionaries.
    """
    DEPLOYMENT_NAME = ("", "deployment_name", "$root")
    SOURCE_TYPE = (MappingGroups.BASE, "source_type", "$root.source.type", _UPPERCASE_MAPPER)
    TARGET_HOSTS = (MappingGroups.BASE, "target_hosts", "$root.target.hosts")
    EXEC_TYPE = (MappingGroups.BASE, "exec_type", "$root.execution.via", _UPPERCASE_MAPPER)

    SOURCE_HOME = (MappingGroups.SOURCE_COMMON, "src_home", "$root.source.home")
    BINARY_NAME = (MappingGroups.SOURCE_COMMON, "src_bin_name", "$root.source.resource")
    RUNTIME_NAME = ("", "runtime_name", "$root.runtime")
    EXEC_COMMAND_NAME = ("", "exec_cmd_name", "$root.execution.command-name")
    EXEC_USER = ("", "exec_user", "$root.execution.as-user")
    EXEC_ARGS = ("", "exec_args", "$root.execution.args")
    EXEC_ARGS_DOCKER_PORTS = (MappingGroups.DOCKER_EXEC_ARGS, "exec_args_docker_ports", "$root.execution.args.ports")
    EXEC_ARGS_DOCKER_ENV = (MappingGroups.DOCKER_EXEC_ARGS, "exec_args_docker_env", "$root.execution.args.environment")
    EXEC_ARGS_DOCKER_VOLUMES = (MappingGroups.DOCKER_EXEC_ARGS, "exec_args_docker_volumes", "$root.execution.args.volumes")
    EXEC_ARGS_DOCKER_NETWORK = (MappingGroups.DOCKER_EXEC_ARGS, "exec_args_docker_network", "$root.execution.args.network-mode")
    EXEC_ARGS_DOCKER_RESTART = (MappingGroups.DOCKER_EXEC_ARGS, "exec_args_docker_restart", "$root.execution.args.restart-policy")
    EXEC_ARGS_DOCKER_CMD = (MappingGroups.DOCKER_EXEC_ARGS, "exec_args_docker_cmd", "$root.execution.args.command-args")

    HEALTH_CHECK_ENABLE = (MappingGroups.BASE, "hc_enable", "$root.health-check.enabled", _DEFAULT_OPTIONS_TO_BOOLEAN_MAPPER)
    HEALTH_CHECK_DELAY = (MappingGroups.HEALTH_CHECK, "hc_delay", "$root.health-check.delay")
    HEALTH_CHECK_TIMEOUT = (MappingGroups.HEALTH_CHECK, "hc_timeout", "$root.health-check.timeout")
    HEALTH_CHECK_MAX_ATTEMPTS = (MappingGroups.HEALTH_CHECK, "hc_max_attempts", "$root.health-check.max-attempts", _STR_TO_INT_MAPPER)
    HEALTH_CHECK_ENDPOINT = (MappingGroups.HEALTH_CHECK, "hc_endpoint", "$root.health-check.endpoint")

    INFO_ENABLE = (MappingGroups.BASE, "info_enable", "$root.info.enabled", _DEFAULT_OPTIONS_TO_BOOLEAN_MAPPER)
    INFO_ENDPOINT = (MappingGroups.INFO, "info_endpoint", "$root.info.endpoint")
    INFO_FIELD_MAPPING = (MappingGroups.INFO, "info_field_mapping", "$root.info.field-mapping")

    RESULT_RENDERING = ("", "result_rendering", None)
