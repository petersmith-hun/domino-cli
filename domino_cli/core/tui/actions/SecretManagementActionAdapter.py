from enum import Enum

from textual.app import App
from textual.message import Message

from domino_cli.core.domain.CustomExceptions import DominoServiceException
from domino_cli.core.service.SecretService import SecretService
from domino_cli.core.tui.actions import LongRunningActionAdapter


class SecretManagementOperation(Enum):
    LOCK = "lock"
    UNLOCK = "unlock"
    DELETE = "delete"


class SecretManagementMessage:
    def __init__(self, secret_key: str, operation: SecretManagementOperation):
        self.secret_key = secret_key
        self.operation = operation


class SecretManagementActionAdapter(LongRunningActionAdapter[SecretManagementMessage]):
    class SecretListRefreshMessage(Message):
        def __init__(self):
            super().__init__()

    def __init__(self, app: App, secret_service: SecretService):
        super().__init__(app)
        self._secret_service = secret_service

    def _action(self, event: SecretManagementMessage):

        try:
            if event.operation == SecretManagementOperation.LOCK:
                self._secret_service.lock_secret(event.secret_key)

            elif event.operation == SecretManagementOperation.UNLOCK:
                self._secret_service.unlock_secret(event.secret_key)

            elif event.operation == SecretManagementOperation.DELETE:
                self._secret_service.delete_secret(event.secret_key)

            past_tense_suffix = "d" if event.operation == SecretManagementOperation.DELETE else "ed"
            self._app.notify(f"Successfully [i]{event.operation.value}{past_tense_suffix}[/i] secret [i]{event.secret_key}[/i]",
                             title="Secret management operation completed", severity="information", markup=True, timeout=10)

            self._app.post_message(self.SecretListRefreshMessage())

        except DominoServiceException as exc:
            self._app.notify(f"Failed to [i]{event.operation.value}[/i] secret [i]{event.secret_key}[/i]: {str(exc)}",
                             title="Secret management operation failed", severity="error", markup=True, timeout=10)
