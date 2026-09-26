from textual.app import App

from domino_cli.core.service.AuthenticationService import AuthenticationService
from domino_cli.core.service.DominoService import DominoService
from domino_cli.core.service.SecretService import SecretService
from domino_cli.core.tui.actions.AuthenticateActionAdapter import AuthenticateActionAdapter
from domino_cli.core.tui.actions.CreateSecretActionAdapter import CreateSecretActionAdapter
from domino_cli.core.tui.actions.DeploymentListActionAdapter import DeploymentListActionAdapter
from domino_cli.core.tui.modals.AuthUtilOptionsModal import AuthUtilOptionsModal
from domino_cli.core.tui.modals.CreateSecretModal import CreateSecretModal
from domino_cli.core.tui.modals.DeploymentDescriptorImportModal import DeploymentDescriptorImportModal
from domino_cli.core.tui.modals.DeploymentOptionsModal import DeploymentOptionsModal
from domino_cli.core.tui.screens.DeploymentListScreen import DeploymentsListScreen
from domino_cli.core.tui.screens.SecretListScreen import SecretListScreen


class TUIMainComponentsFactory:

    def __init__(self, authentication_service: AuthenticationService, domino_service: DominoService, secret_service: SecretService):
        self._authentication_service = authentication_service
        self._domino_service = domino_service
        self._secret_service = secret_service

    def create_auth_util_options_modal(self) -> AuthUtilOptionsModal:
        return AuthUtilOptionsModal(self._authentication_service)

    def create_authenticate_action_adapter(self, app: App) -> AuthenticateActionAdapter:
        return AuthenticateActionAdapter(app, self._authentication_service)

    def create_deployment_list_screen(self) -> DeploymentsListScreen:
        return DeploymentsListScreen(self._domino_service)

    def create_deployment_options_modal(self, deployment_id: str) -> DeploymentOptionsModal:
        return DeploymentOptionsModal(self._domino_service, deployment_id)

    def create_deployment_list_action_adapter(self, app: App) -> DeploymentListActionAdapter:
        return DeploymentListActionAdapter(app, self._domino_service)

    def create_deployment_descriptor_import_modal(self) -> DeploymentDescriptorImportModal:
        return DeploymentDescriptorImportModal(self._domino_service)

    def create_secret_list_screen(self) -> SecretListScreen:
        return SecretListScreen(self._secret_service)

    def create_create_secret_modal(self) -> CreateSecretModal:
        return CreateSecretModal(self._secret_service)

    def create_create_secret_action_adapter(self, app: App) -> CreateSecretActionAdapter:
        return CreateSecretActionAdapter(app, self._secret_service)
