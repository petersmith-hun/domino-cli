import os
from typing import Optional

from domino_cli.core.cli.Logging import warning
from domino_cli.core.domain.SessionContext import SessionContext


class SessionContextHolder:
    """
    Component holding the currently active session context object.
    """
    def __init__(self):
        self._session_context = None

        preauthorized_token = os.getenv("DOMINO_CLI_PREAUTHORIZED_TOKEN")
        if preauthorized_token is not None:
            self._session_context = SessionContext("preauthorized", preauthorized_token)

    def update(self, session_context: SessionContext) -> None:
        """
        Updates session context.
        """
        self._session_context = session_context

    def get_bearer_auth(self) -> Optional[dict]:

        bearer_auth = None
        if self._session_context is None:
            warning("Session is not yet open!")
        else:
            bearer_auth = {"Authorization": "Bearer {0}".format(self._session_context.authentication_token)}

        return bearer_auth
