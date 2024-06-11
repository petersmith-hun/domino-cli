from core.service.wizard.mapping.WizardDataMappingBaseEnum import WizardDataMappingBaseEnum


class DeploymentConfigWizardDataMapping(WizardDataMappingBaseEnum):
    """
    Field mappings between raw wizard response data and target data dictionaries.
    """
    DEPLOYMENT_NAME = ("deployment_name", "$root")
    SOURCE_TYPE = ("source_type", "$root.source.type")
    TARGET_HOSTS = ("target_hosts", "$root.target.hosts")
    EXEC_TYPE = ("exec_type", "$root.execution.via")
    SOURCE_HOME = ("src_home", "$root.source.home")
    BINARY_NAME = ("src_bin_name", "$root.source.resource")
    RUNTIME_NAME = ("runtime_name", "$root.runtime")
    EXEC_COMMAND_NAME = ("exec_cmd_name", "$root.execution.command-name")
    EXEC_USER = ("exec_user", "$root.execution.as-user")
    EXEC_ARGS = ("exec_args", "$root.execution.args")
    EXEC_ARGS_DOCKER_PORTS = ("exec_args_docker_ports", "$root.execution.args.ports")
    EXEC_ARGS_DOCKER_ENV = ("exec_args_docker_env", "$root.execution.args.environment")
    EXEC_ARGS_DOCKER_VOLUMES = ("exec_args_docker_volumes", "$root.execution.args.volumes")
    EXEC_ARGS_DOCKER_NETWORK = ("exec_args_docker_network", "$root.execution.args.network-mode")
    EXEC_ARGS_DOCKER_RESTART = ("exec_args_docker_restart", "$root.execution.args.restart-policy")
    EXEC_ARGS_DOCKER_CMD = ("exec_args_docker_cmd", "$root.execution.args.command-args")
    HEALTH_CHECK_ENABLE = ("hc_enable", "$root.health-check.enabled")
    HEALTH_CHECK_DELAY = ("hc_delay", "$root.health-check.delay")
    HEALTH_CHECK_TIMEOUT = ("hc_timeout", "$root.health-check.timeout")
    HEALTH_CHECK_MAX_ATTEMPTS = ("hc_max_attempts", "$root.health-check.max-attempts")
    HEALTH_CHECK_ENDPOINT = ("hc_endpoint", "$root.health-check.endpoint")
    INFO_ENABLE = ("info_enable", "$root.info.enabled")
    INFO_ENDPOINT = ("info_endpoint", "$root.info.endpoint")
    INFO_FIELD_MAPPING = ("info_field_mapping", "$root.info.field-mapping")
    RESULT_RENDERING = ("result_rendering", None)
