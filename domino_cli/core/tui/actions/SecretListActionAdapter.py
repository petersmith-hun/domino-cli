from textual.app import App
from textual.widgets import ListView

from domino_cli.core.service.SecretService import SecretService
from domino_cli.core.tui.actions import LongRunningActionAdapter
from domino_cli.core.tui.screens.SecretListScreen import SecretListHeader, SecretListItem, ContextListItem


class SecretListActionAdapter(LongRunningActionAdapter[None]):

    def __init__(self, app: App, secret_service: SecretService):
        super().__init__(app)
        self._secret_service = secret_service

    def _action(self, event: None):

        try:
            secrets_groups = self._secret_service.get_all_metadata()

        except Exception as exc:
            self._app.call_from_thread(lambda: self._app.notify(f"Error fetching secrets: {str(exc)}", title="Failed fetching secrets", severity="error"))
            return

        if secrets_groups is None or len(secrets_groups) == 0:
            return

        secrets_list_view = self._app.query_one("#secrets", ListView)

        if secrets_list_view.children:
            self._app.call_from_thread(lambda: secrets_list_view.clear())

        self._app.call_from_thread(lambda: secrets_list_view.append(SecretListHeader()))

        for secret_group in secrets_groups:
            self._app.call_from_thread(lambda: secrets_list_view.append(ContextListItem(secret_group)))

            for secret in secret_group.secrets:
                self._app.call_from_thread(lambda: secrets_list_view.append(SecretListItem(secret)))
