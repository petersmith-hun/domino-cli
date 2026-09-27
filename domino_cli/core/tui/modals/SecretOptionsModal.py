from typing import List

from textual.widgets import Label

from domino_cli.core.domain.Secrets import SecretDetails
from domino_cli.core.service.SecretService import SecretService
from domino_cli.core.tui.actions.SecretManagementActionAdapter import SecretManagementOperation, \
    SecretManagementActionAdapter, SecretManagementMessage
from domino_cli.core.tui.modals import ConfirmationModal, OptionsModalScreen, CustomModalListItem
from domino_cli.core.tui.modals.RetrievedSecretsModal import RetrievedSecretsModal


class SecretOptionsModal(OptionsModalScreen):

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
        super().__init__()
        self._secret_service = secret_service
        self._secret_details = secret
        self._secret_management_action_adapter = SecretManagementActionAdapter(self.app, self._secret_service)

    def _get_title(self) -> Label:
        return Label(self._secret_details.key)

    def _get_sub_title(self) -> Label:
        return Label("ⓘ Secret options")

    def _get_items(self) -> List[CustomModalListItem]:

        options: List[CustomModalListItem] = []
        if self._secret_details.retrievable:
            options.append(CustomModalListItem("retrieve_secret", "Retrieve secret",
                                               "Retrieves this secret in decrypted form"))
            options.append(CustomModalListItem("lock_secret", "Lock secret",
                                               "Locks this secret, making it only accessible by Domino Coordinator"))
        else:
            options.append(CustomModalListItem("unlock_secret", "Unlock secret",
                                               "Unlocks this secret, making it retrievable via API"))

        options.append(CustomModalListItem("delete_secret", "Delete secret",
                                           "Deletes this secret. This operation is permanent, and might lead to deployment failures"))

        return options

    def _on_option_selected(self, item_id: str) -> None:

        if item_id == "retrieve_secret":
            self.loading = True
            self.run_worker(self._handle_secret_retrieval, thread=True)

        else:
            message = SecretManagementMessage(self._secret_details.key, self._operation_map[item_id])
            callback = lambda: self._secret_management_action_adapter.execute(message)
            self.app.push_screen(ConfirmationModal(self._confirmation_map[item_id], callback))

    def _handle_secret_retrieval(self) -> None:
        secrets = self._secret_service.retrieve_secret_by_key(self._secret_details.key)
        self.app.call_from_thread(lambda: self.app.push_screen(RetrievedSecretsModal(secrets)))
        self.loading = False
