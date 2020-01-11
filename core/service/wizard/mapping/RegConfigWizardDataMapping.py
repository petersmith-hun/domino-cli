from core.service.wizard.mapping.WizardDataMappingBaseEnum import WizardDataMappingBaseEnum


class RegConfigWizardDataMapping(WizardDataMappingBaseEnum):

    REGISTRATION_NAME = ("reg_name", "$root")
    SOURCE_TYPE = ("source_type", "$root.source.type")
    EXEC_TYPE = ("exec_type", "$root.execution.via")
    SOURCE_HOME = ("src_home", "$root.source.home")
    BINARY_NAME = ("src_bin_name", "$root.source.resource")
    RUNTIME_NAME = ("runtime_name", "$root.runtime")
    EXEC_COMMAND_NAME = ("exec_cmd_name", "$root.execution.command-name")
    EXEC_USER = ("exec_user", "$root.execution.as-user")
    EXEC_ARGS = ("exec_args", "$root.execution.args")
    HEALTH_CHECK_ENABLE = ("hc_enable", "$root.health-check.enabled")
    HEALTH_CHECK_DELAY = ("hc_delay", "$root.health-check.delay")
    HEALTH_CHECK_TIMEOUT = ("hc_timeout", "$root.health-check.timeout")
    HEALTH_CHECK_MAX_ATTEMPTS = ("hc_max_attempts", "$root.health-check.max-attempts")
    HEALTH_CHECK_ENDPOINT = ("hc_endpoint", "$root.health-check.endpoint")
    RESULT_RENDERING = ("result_rendering", None)
