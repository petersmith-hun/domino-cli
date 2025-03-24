import subprocess
from abc import ABC, abstractmethod
from typing import List

from domino_cli.core.cli.Logging import info, warning
from domino_cli.core.cli.RuntimeHelper import RuntimeHelper
from domino_cli.core.service.wizard.installer import VersionResolver
from domino_cli.core.service.wizard.mapping.InstallerWizardDataMapping import Mapping
from domino_cli.core.service.wizard.mapping.WizardDataMappingBaseEnum import WizardDataMappingBaseEnum
from domino_cli.installer_config import DominoComponent


class PlatformComponentInstaller(ABC):
    """
    Abstract base implementation for Domino Platform component installers.
    """
    def __init__(self, version_resolver: VersionResolver):
        self._version_resolver = version_resolver

    def install(self, wizard_data: dict) -> None:
        """
        Installs the given component by preparing a set of Shell calls and passes them to the backing system.
        :param wizard_data: raw wizard data to extract installation parameters from
        """
        component = self._extract_value(wizard_data, Mapping.COMPONENT)
        info("Preparing to install {0} as {1} ...".format(component.value, self._reported_installation_method()))
        info("Looking up latest version of component {0}, please wait ...".format(component.value))
        version = self._version_resolver.resolve_latest(component)
        command_lines = self._prepare_command_lines(component, wizard_data, version)

        info("{0} {1} will be installed. Do you wish to proceed? (Type 'yes' to proceed)"
              .format(component.value, version))
        if RuntimeHelper.input_wrapper(lambda: input()) != "yes":
            warning("Installation aborted")
            return

        [subprocess.call(command_line) for command_line in command_lines]

    @abstractmethod
    def _prepare_command_lines(self, component: DominoComponent, wizard_data: dict, version: str) -> List[List[str]]:
        """
        Actual installer implementations must return a set of Shell calls in order to install the component.
        :param component: DominoComponent reference of the component to be installed
        :param wizard_data: raw wizard data to extract installation parameters from
        :param version: version to be installed
        :return: list of commands (each command split into an array by space) to be passed to subprocess
        """
        pass

    @abstractmethod
    def _reported_installation_method(self) -> str:
        """
        Returns an installation method indicator description of the actual installer.
        :return: installation method indicator description
        """
        pass

    @staticmethod
    def _extract_value(wizard_data: dict, mapping: WizardDataMappingBaseEnum) -> any:
        return mapping.get_mapper()(wizard_data[mapping.get_wizard_field()])
