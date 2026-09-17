from textual.app import App
from textual.message import Message

from domino_cli.core.domain.CustomExceptions import DominoServiceException
from domino_cli.core.service.SecretService import SecretService
from domino_cli.core.tui.actions import LongRunningActionAdapter


class NewSecret:
    def __init__(self, secret_context, secret_key, secret_value):
        self.secret_context = secret_context
        self.secret_key = secret_key
        self.secret_value = secret_value


class CreateSecretActionAdapter(LongRunningActionAdapter[NewSecret]):
    class SecretCreatedMessage(Message):
        def __init__(self):
            super().__init__()

    def __init__(self, app: App, secret_service: SecretService):
        super().__init__(app)
        self._secret_service = secret_service

    def _action(self, event: NewSecret):

        try:
            self._secret_service.create_secret(event.secret_key, event.secret_context, event.secret_value)
            self._app.notify(f"Secret [i]{event.secret_key}[/i] has been created successfully",
                             title="Secret creation successful", markup=True, severity="information")
            self._app.post_message(CreateSecretActionAdapter.SecretCreatedMessage())

        except DominoServiceException as exc:
            self._app.call_from_thread(lambda: self._app.notify(f"Error creating secrets {str(exc)}",
                                                                title="Secret creation failed", severity="error"))
            return
