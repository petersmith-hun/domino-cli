from abc import ABC, abstractmethod

from core.domain.AuthMode import AuthMode
from core.domain.SessionContext import SessionContext


class AbstractAuthHandler(ABC):
    """
    Implementation of this class should be able to handle authentication process with Domino.
    The result should always be a SessionContext object, containing the authenticated username and an access token.
    """

    @abstractmethod
    def create_session_context(self) -> SessionContext:
        """
        Requests authentication and generates a SessionContext object based on the result.

        :return: populated SessionContext object
        """
        pass

    @abstractmethod
    def for_auth_mode(self) -> AuthMode:
        """
        Returns the assigned authentication mode as AuthMode.

        :return: the assigned authentication mode as AuthMode
        """
        pass
