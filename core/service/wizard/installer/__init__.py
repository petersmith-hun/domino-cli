from abc import ABC, abstractmethod

from installer_config import DominoComponent


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
