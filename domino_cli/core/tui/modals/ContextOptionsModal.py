from typing import List

from textual.widget import Widget
from textual.widgets import Label, OptionList
from textual.widgets.option_list import Option

from domino_cli.core.service.SecretService import SecretService
from domino_cli.core.tui.modals import CustomModalScreen
from domino_cli.core.tui.modals.RetrievedSecretsModal import RetrievedSecretsModal


class ContextOptionsModal(CustomModalScreen):

    def __init__(self, secret_service: SecretService, secret_context: str):
        super().__init__("")
        self._secret_service = secret_service
        self._secret_context = secret_context

    def _get_title(self) -> Label:
        return Label(f"{self._secret_context} secret context options")

    def _get_content(self) -> List[Widget]:
        return [ContextOptionList(self._secret_service, self._secret_context)]


class ContextOptionList(OptionList):

    def __init__(self, secret_service: SecretService, secret_context: str):
        super().__init__(
            Option("Retrieve all secrets in context", id="retrieve_context")
        )
        self._secret_service = secret_service
        self._secret_context = secret_context

    def action_select(self) -> None:
        self.loading = True
        self.run_worker(self._handle_secret_retrieval, thread=True)

    def _handle_secret_retrieval(self) -> None:
        secrets = self._secret_service.retrieve_secrets_by_context(self._secret_context)
        self.app.call_from_thread(lambda: self.app.push_screen(RetrievedSecretsModal(secrets)))
        self.loading = False
