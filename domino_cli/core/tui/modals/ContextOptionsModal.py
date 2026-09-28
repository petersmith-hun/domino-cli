from typing import List

from textual.widgets import Label

from domino_cli.core.service.SecretService import SecretService
from domino_cli.core.tui.modals import OptionsModalScreen, CustomModalListItem
from domino_cli.core.tui.modals.RetrievedSecretsModal import RetrievedSecretsModal


class ContextOptionsModal(OptionsModalScreen):

    def __init__(self, secret_service: SecretService, secret_context: str):
        super().__init__()
        self._secret_service = secret_service
        self._secret_context = secret_context

    def _get_title(self) -> Label:
        return Label(self._secret_context)

    def _get_sub_title(self) -> Label:
        return Label("ⓘ Secret context options")

    def _get_items(self) -> List[CustomModalListItem]:
        return [
            CustomModalListItem("retrieve_context", "Retrieve all secrets in context",
                                "Retrieves all secrets in this context in decrypted form")
        ]

    def _on_option_selected(self, item_id: str) -> None:
        self.loading = True
        self.run_worker(self._handle_secret_retrieval, thread=True)

    def _handle_secret_retrieval(self) -> None:

        try:
            secrets = self._secret_service.retrieve_secrets_by_context(self._secret_context)
            self.app.call_from_thread(lambda: self.app.push_screen(RetrievedSecretsModal(secrets)))

        except Exception as exc:
            self.app.notify(f"Failed to retrieve secrets: {str(exc)}", title="Secret retrieval failed", severity="error")

        finally:
            self.loading = False
