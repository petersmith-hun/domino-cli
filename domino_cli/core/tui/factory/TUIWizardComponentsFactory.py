from typing import List, TypeVar

from domino_cli.core.service.wizard.installer import InstallerType
from domino_cli.core.service.wizard.installer.PlatformComponentInstaller import PlatformComponentInstaller
from domino_cli.core.service.wizard.transformer import WizardTransformerType
from domino_cli.core.service.wizard.transformer.AbstractWizardResultTransformer import AbstractWizardResultTransformer
from domino_cli.core.tui.modals.wizards import BaseWizardModal
from domino_cli.core.tui.modals.wizards.BinaryExecutableAgentConfigWizardModal import \
    BinaryExecutableAgentConfigWizardModal
from domino_cli.core.tui.modals.wizards.CoordinatorConfigWizardModal import CoordinatorConfigWizardModal
from domino_cli.core.tui.modals.wizards.DeploymentDefinitionWizardModal import DeploymentDefinitionWizardModal
from domino_cli.core.tui.modals.wizards.DockerAgentConfigWizardModal import DockerAgentConfigWizardModal
from domino_cli.core.tui.modals.wizards.InstallerWizardModal import InstallerWizardModal
from domino_cli.core.tui.screens.WizardSelectorScreen import WizardSelectorScreen


T = TypeVar("T", bound=AbstractWizardResultTransformer)


class TUIWizardComponentsFactory:
    def __init__(self, wizard_result_transformers: List[T], platform_component_installers: List[PlatformComponentInstaller]):
        self._wizard_result_transformers_map = {transformer.transformer_type(): transformer for transformer in wizard_result_transformers}
        self._platform_component_installers_map = {installer.installer_type(): installer for installer in platform_component_installers}

    def create_wizard_selector_screen(self) -> WizardSelectorScreen:
        return WizardSelectorScreen(lambda wizard_id: self._wizard_modal_factory(wizard_id))
    
    def _wizard_modal_factory(self, wizard_id: str) -> BaseWizardModal | None:

        if wizard_id == "wizard_deployment_definition":
            return DeploymentDefinitionWizardModal(self._get_transformer(WizardTransformerType.DEPLOYMENT_CONFIG))

        elif wizard_id == "wizard_coordinator":
            return CoordinatorConfigWizardModal(self._get_transformer(WizardTransformerType.COORDINATOR_CONFIG))

        elif wizard_id == "wizard_docker_agent_config":
            return DockerAgentConfigWizardModal(self._get_transformer(WizardTransformerType.DOCKER_AGENT_CONFIG))

        elif wizard_id == "wizard_bin_exec_agent":
            return BinaryExecutableAgentConfigWizardModal(self._get_transformer(WizardTransformerType.BINARY_EXECUTABLE_AGENT_CONFIG))

        elif wizard_id == "wizard_installer":
            return InstallerWizardModal(lambda current_component: self._resolve_installer(current_component))

        return None

    def _get_transformer(self, transformer_type: WizardTransformerType) -> T:
        return self._wizard_result_transformers_map[transformer_type]

    def _resolve_installer(self, current_component: str) -> PlatformComponentInstaller:

        if current_component in ["coordinator", "docker-agent"]:
            return self._platform_component_installers_map[InstallerType.DOCKER_BASED_INSTALLER]
        else:
            return self._platform_component_installers_map[InstallerType.BINARY_EXECUTABLE_BASED_INSTALLER]
