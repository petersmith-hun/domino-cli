from enum import Enum

from core.service.wizard.mapping.WizardDataMappingBaseEnum import WizardDataMappingBaseEnum


class MappingGroups(Enum):
    BASE = "base"
    FIRST_RUNTIME = "first-runtime"


class Mapping(WizardDataMappingBaseEnum):
    """
    Field mappings between raw wizard response data and target data dictionaries for Binary Executable Agent configuration.
    """
    SPAWN_CONTROL_SERVICE_HANDLER = (MappingGroups.BASE, "spawn_control_service_handler", "$root.spawn-control.service-handler")
    SPAWN_CONTROL_START_DELAY = (MappingGroups.BASE, "spawn_control_start_delay", "$root.spawn-control.start-delay")
    SPAWN_CONTROL_EXEC_USERS = (MappingGroups.BASE, "spawn_control_exec_users", "$root.spawn-control.allowed-executor-users")

    STORAGE_DEPLOYMENTS = (MappingGroups.BASE, "storage_deployments_store", "$root.storage.deployment-store-path")
    STORAGE_APP_HOME = (MappingGroups.BASE, "storage_app_home", "$root.storage.application-home-path")

    RUNTIME_CONFIGURE_FIRST = ("", "runtime_configure_first", "$root.runtimes")
    RUNTIME_ID = (MappingGroups.FIRST_RUNTIME, "runtime_id", "id")
    RUNTIME_BINARY_PATH = (MappingGroups.FIRST_RUNTIME, "runtime_binary_path", "binary-path")
    RUNTIME_HEALTHCHECK = (MappingGroups.FIRST_RUNTIME, "runtime_healthcheck", "healthcheck")
    RUNTIME_COMMAND_LINE = (MappingGroups.FIRST_RUNTIME, "runtime_command_line", "command-line")
