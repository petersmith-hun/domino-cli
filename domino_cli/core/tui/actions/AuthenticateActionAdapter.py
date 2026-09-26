from textual.app import App

from domino_cli.core.domain.CustomExceptions import AuthenticationException
from domino_cli.core.service.AuthenticationService import AuthenticationService
from domino_cli.core.tui.TUIRuntimeHelper import TUIRuntimeHelper
from domino_cli.core.tui.actions import LongRunningActionAdapter


class AuthenticateActionAdapter(LongRunningActionAdapter[None]):
    def __init__(self, app: App, authentication_service: AuthenticationService):
        super().__init__(app)
        self._authentication_service = authentication_service

    def _action(self, event: None):
        try:
            session_context = self._authentication_service.open_session()
            TUIRuntimeHelper.set_authenticated(session_context, self._app)
            self._app.notify(f"Welcome, [i]{self._authentication_service.get_username()}[/i]", title="Session is open", severity="information", markup=True)

        except AuthenticationException as exc:
            self._app.notify(str(exc), title="Authentication failed", severity="error")
