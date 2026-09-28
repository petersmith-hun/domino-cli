from abc import ABC, abstractmethod
from enum import Enum

from domino_cli.installer_config import DominoComponent


class VersionResolver(ABC):
    """
    Implementations of this interface must be able to resolve versions of the given component.
    """

    @abstractmethod
    def resolve_latest(self, component: DominoComponent) -> str:
        """
        Resolves the latest version of the given component.
        :param component: component under installation to resolve the latest version of
        :return: resolved latest version
        """
        pass


class InstallerType(Enum):
    DOCKER_BASED_INSTALLER = "docker_based"
    BINARY_EXECUTABLE_BASED_INSTALLER = "binary_executable_based"
