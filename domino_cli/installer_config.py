from enum import Enum


class DominoComponent(Enum):
    """
    Supported Domino Platform components.
    """
    COORDINATOR = "coordinator"
    DOCKER_AGENT = "docker-agent"
    BIN_EXEC_AGENT = "binary-executable-agent"


class InstallerConfig:
    """
    Installer common static parameters.
    """
    def __init__(self):
        self.docker_registry = "docker.io/psproghu"
        self.executable_source = "https://github.com/petersmith-hun/domino-platform/releases/download/{component}-linux-x64-v{version}-release/domino-{component}"
        self.docker_version_source = "https://hub.docker.com/v2/namespaces/psproghu/repositories/domino-{component}/tags"
        self.github_release_version_source = "https://api.github.com/repos/petersmith-hun/domino-platform/releases"
        self.component_installed_name = {
            DominoComponent.COORDINATOR: "domino-coordinator",
            DominoComponent.DOCKER_AGENT: "domino-docker-agent",
            DominoComponent.BIN_EXEC_AGENT: "domino-bin-exec-agent"

        }
        self.docker_container_heap_size = {
            DominoComponent.COORDINATOR: 128,
            DominoComponent.DOCKER_AGENT: 64
        }


installer_config = InstallerConfig()
