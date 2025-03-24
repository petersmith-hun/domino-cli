import os

from domino_cli.core.cli.CLI import CLI
from domino_cli.core.cli.Logging import info
from domino_cli.core.client.DominoClient import DominoClient
from domino_cli.core.client.OAuthAuthorizationClient import OAuthAuthorizationClient
from domino_cli.core.command.AuthCommand import AuthCommand
from domino_cli.core.command.DeployApplicationCommand import DeployApplicationCommand
from domino_cli.core.command.ExitCommand import ExitCommand
from domino_cli.core.command.HelpCommand import HelpCommand
from domino_cli.core.command.InfoCommand import InfoCommand
from domino_cli.core.command.RestartApplicationCommand import RestartApplicationCommand
from domino_cli.core.command.StartApplicationCommand import StartApplicationCommand
from domino_cli.core.command.StopApplicationCommand import StopApplicationCommand
from domino_cli.core.command.WizardCommand import WizardCommand
from domino_cli.core.domain.AuthMode import AuthMode
from domino_cli.core.domain.OAuthConfig import OAuthConfig
from domino_cli.core.service.AuthenticationService import AuthenticationService
from domino_cli.core.service.CommandProcessor import CommandProcessor
from domino_cli.core.service.ConfigurationWizardService import ConfigurationWizardService
from domino_cli.core.service.DominoService import DominoService
from domino_cli.core.service.SessionContextHolder import SessionContextHolder
from domino_cli.core.service.auth.DirectAuthHandler import DirectAuthHandler
from domino_cli.core.service.auth.OAuthAuthHandler import OAuthAuthHandler
from domino_cli.core.service.wizard.BinaryExecutableAgentConfigWizard import BinaryExecutableAgentConfigWizard
from domino_cli.core.service.wizard.CoordinatorConfigWizard import CoordinatorConfigWizard
from domino_cli.core.service.wizard.DeploymentConfigWizard import DeploymentConfigWizard
from domino_cli.core.service.wizard.DockerAgentConfigWizard import DockerAgentConfigWizard
from domino_cli.core.service.wizard.InstallerWizard import InstallerWizard
from domino_cli.core.service.wizard.installer.BinaryExecutablePlatformComponentInstaller import \
    BinaryExecutablePlatformComponentInstaller
from domino_cli.core.service.wizard.installer.DockerPlatformComponentInstaller import DockerPlatformComponentInstaller
from domino_cli.core.service.wizard.installer.DockerVersionResolver import DockerVersionResolver
from domino_cli.core.service.wizard.installer.GitHubReleaseVersionResolver import GitHubReleaseVersionResolver
from domino_cli.core.service.wizard.render.WizardResultConsoleRenderer import WizardResultConsoleRenderer
from domino_cli.core.service.wizard.render.WizardResultFileRenderer import WizardResultFileRenderer
from domino_cli.core.service.wizard.transformer.BinaryExecutableAgentConfigWizardResultTransformer import \
    BinaryExecutableAgentConfigWizardResultTransformer
from domino_cli.core.service.wizard.transformer.CoordinatorConfigWizardResultTransformer import \
    CoordinatorConfigWizardResultTransformer
from domino_cli.core.service.wizard.transformer.DeploymentConfigWizardResultTransformer import \
    DeploymentConfigWizardResultTransformer
from domino_cli.core.service.wizard.transformer.DockerAgentConfigWizardResultTransformer import \
    DockerAgentConfigWizardResultTransformer


class ApplicationContext:
    """
    Simple IoC container for Domino CLI.
    """
    @staticmethod
    def init_cli(version: str) -> CLI:

        info("Initializing Domino CLI...")

        # configuration properties
        _domino_base_url = ApplicationContext._assert_config_value("DOMINO_BASE_URL")
        _default_auth_mode = AuthMode.by_value(os.getenv("DOMINO_DEFAULT_AUTH_MODE", AuthMode.DIRECT.value))
        _oauth_config = OAuthConfig()

        # wizards
        _wizard_result_console_renderer = WizardResultConsoleRenderer()
        _wizard_result_file_renderer = WizardResultFileRenderer()
        _deployment_config_wizard_result_transformer = DeploymentConfigWizardResultTransformer()
        _coordinator_config_wizard_result_transformer = CoordinatorConfigWizardResultTransformer()
        _docker_agent_config_wizard_result_transformer = DockerAgentConfigWizardResultTransformer()
        _bin_exec_agent_config_wizard_result_transformer = BinaryExecutableAgentConfigWizardResultTransformer()
        _deployment_config_wizard = DeploymentConfigWizard(_deployment_config_wizard_result_transformer,
                                                           _wizard_result_console_renderer,
                                                           _wizard_result_file_renderer)
        _coordinator_config_wizard = CoordinatorConfigWizard(_coordinator_config_wizard_result_transformer,
                                                             _wizard_result_console_renderer,
                                                             _wizard_result_file_renderer)
        _docker_agent_config_wizard = DockerAgentConfigWizard(_docker_agent_config_wizard_result_transformer,
                                                              _wizard_result_console_renderer,
                                                              _wizard_result_file_renderer)
        _bin_exec_agent_config_wizard = BinaryExecutableAgentConfigWizard(_bin_exec_agent_config_wizard_result_transformer,
                                                                          _wizard_result_console_renderer,
                                                                          _wizard_result_file_renderer)

        # installer
        _docker_version_resolver = DockerVersionResolver()
        _github_release_version_resolver = GitHubReleaseVersionResolver()
        _docker_platform_component_installer = DockerPlatformComponentInstaller(_docker_version_resolver)
        _bin_exec_platform_component_installer = BinaryExecutablePlatformComponentInstaller(_github_release_version_resolver)
        _installer_wizard = InstallerWizard(_docker_platform_component_installer, _bin_exec_platform_component_installer)

        # common components
        _session_context_holder = SessionContextHolder()
        _domino_client = DominoClient(_domino_base_url, _session_context_holder)
        _oauth_authorization_client = OAuthAuthorizationClient(_oauth_config)
        _domino_service = DominoService(_domino_client)
        _direct_auth_handler = DirectAuthHandler(_domino_client)
        _oauth_auth_handler = OAuthAuthHandler(_oauth_config, _oauth_authorization_client)
        _auth_service = AuthenticationService(_default_auth_mode, _session_context_holder, [
            _direct_auth_handler,
            _oauth_auth_handler
        ])
        _config_wizard_service = ConfigurationWizardService([
            _deployment_config_wizard,
            _coordinator_config_wizard,
            _docker_agent_config_wizard,
            _bin_exec_agent_config_wizard,
            _installer_wizard
        ])

        # commands
        _command_exit = ExitCommand()
        _command_help = HelpCommand()
        _command_start_app = StartApplicationCommand(_domino_service)
        _command_stop_app = StopApplicationCommand(_domino_service)
        _command_restart_app = RestartApplicationCommand(_domino_service)
        _command_deploy_app = DeployApplicationCommand(_domino_service)
        _command_auth = AuthCommand(_auth_service)
        _command_wizard = WizardCommand(_config_wizard_service)
        _command_info = InfoCommand(_domino_service)

        # command processor
        _command_processor = CommandProcessor(_command_help, [
            _command_help,
            _command_exit,
            _command_auth,
            _command_deploy_app,
            _command_restart_app,
            _command_start_app,
            _command_stop_app,
            _command_wizard,
            _command_info
        ])

        _cli = CLI(_command_processor)

        info(f"Domino CLI v{version} initialized")
        info("-" * 30)

        return _cli

    @staticmethod
    def _assert_config_value(config_parameter: str) -> str:

        config_value = os.getenv(config_parameter)
        if config_value is None:
            raise Exception("Configuration parameter {0} is not specified".format(config_parameter))

        return config_value
