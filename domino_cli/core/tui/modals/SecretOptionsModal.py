from typing import List

from textual.widget import Widget
from textual.widgets import Label, OptionList
from textual.widgets.option_list import Option

from domino_cli.core.domain.Secrets import SecretDetails
from domino_cli.core.service.SecretService import SecretService
from domino_cli.core.tui.actions.SecretManagementActionAdapter import SecretManagementOperation, \
    SecretManagementActionAdapter, SecretManagementMessage
from domino_cli.core.tui.modals import CustomModalScreen, ConfirmationModal
from domino_cli.core.tui.modals.RetrievedSecretsModal import RetrievedSecretsModal


class SecretOptionsModal(CustomModalScreen):

    def __init__(self, secret_service: SecretService, secret: SecretDetails):
        super().__init__()
        self._secret_service = secret_service
        self._secret_details = secret

    def _get_title(self) -> Label:
        return Label(f"{self._secret_details.key} secret options")

    def _get_content(self) -> List[Widget]:
        return [SecretOptionList(self._secret_service, self._secret_details)]


class SecretOptionList(OptionList):

    _confirmation_map = {
        "lock_secret": "This operation locks the secret, making it only accessible by Domino Coordinator",
        "unlock_secret": "This operation unlocks the secret, making it retrievable via API",
        "delete_secret": "Deleting this secret is permanent, and might lead to deployment failures",
    }

    _operation_map = {
        "lock_secret": SecretManagementOperation.LOCK,
        "unlock_secret": SecretManagementOperation.UNLOCK,
        "delete_secret": SecretManagementOperation.DELETE,
    }

    def __init__(self, secret_service: SecretService, secret: SecretDetails):

        options: List[Option] = []
        if secret.retrievable:
            options.append(Option("Retrieve secret", id="retrieve_secret"))
            options.append(Option("Lock secret", id="lock_secret"))
        else:
            options.append(Option("Unlock secret", id="unlock_secret"))

        options.append(Option("Delete secret", id="delete_secret"))

        super().__init__(*options)
        self._secret_service = secret_service
        self._secret_details = secret
        self._secret_management_action_adapter = SecretManagementActionAdapter(self.app, self._secret_service)

    def action_select(self) -> None:

        if self.highlighted_option is None:
            return

        option_id = str(self.highlighted_option.id)

        if option_id == "retrieve_secret":
            self.loading = True
            self.run_worker(self._handle_secret_retrieval, thread=True)

        else:
            message = SecretManagementMessage(self._secret_details.key, self._operation_map[option_id])
            callback = lambda: self._secret_management_action_adapter.execute(message)
            self.app.push_screen(ConfirmationModal(self._confirmation_map[option_id], callback))

    def _handle_secret_retrieval(self) -> None:
        secrets = self._secret_service.retrieve_secret_by_key(self._secret_details.key)
        self.app.call_from_thread(lambda: self.app.push_screen(RetrievedSecretsModal(secrets)))
        self.loading = False
