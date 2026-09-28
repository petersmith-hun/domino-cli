from enum import Enum


class WizardTransformerType(Enum):
    BINARY_EXECUTABLE_AGENT_CONFIG = "binary_executable_agent_config"
    COORDINATOR_CONFIG = "coordinator_config"
    DEPLOYMENT_CONFIG = "deployment_config"
    DOCKER_AGENT_CONFIG = "docker_agent_config"
