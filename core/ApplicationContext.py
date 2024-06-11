import os

from core.cli.CLI import CLI
from core.client.DominoClient import DominoClient
from core.client.OAuthAuthorizationClient import OAuthAuthorizationClient
from core.command.AuthCommand import AuthCommand
from core.command.DeployApplicationCommand import DeployApplicationCommand
from core.command.ExitCommand import ExitCommand
from core.command.HelpCommand import HelpCommand
from core.command.InfoCommand import InfoCommand
from core.command.RestartApplicationCommand import RestartApplicationCommand
from core.command.StartApplicationCommand import StartApplicationCommand
from core.command.StopApplicationCommand import StopApplicationCommand
from core.command.WizardCommand import WizardCommand
from core.domain.AuthMode import AuthMode
from core.domain.OAuthConfig import OAuthConfig
from core.service.AuthenticationService import AuthenticationService
from core.service.CommandProcessor import CommandProcessor
from core.service.ConfigurationWizardService import ConfigurationWizardService
from core.service.DominoService import DominoService
from core.service.SessionContextHolder import SessionContextHolder
from core.service.auth.DirectAuthHandler import DirectAuthHandler
from core.service.auth.OAuthAuthHandler import OAuthAuthHandler
from core.service.wizard.DeploymentConfigWizard import DeploymentConfigWizard
from core.service.wizard.render.WizardResultConsoleRenderer import WizardResultConsoleRenderer
from core.service.wizard.render.WizardResultFileRenderer import WizardResultFileRenderer
from core.service.wizard.transformer.DeploymentConfigWizardResultTransformer import DeploymentConfigWizardResultTransformer


class ApplicationContext:
    """
    Simple IoC container for Domino CLI.
    """
    @staticmethod
    def init_cli(version: str) -> CLI:

        print("Initializing Domino CLI...")

        # configuration properties
        _domino_base_url = ApplicationContext._assert_config_value("DOMINO_BASE_URL")
        _default_auth_mode = AuthMode.by_value(os.getenv("DOMINO_DEFAULT_AUTH_MODE", AuthMode.DIRECT.value))
        _oauth_config = OAuthConfig()

        # wizards
        _wizard_result_console_renderer = WizardResultConsoleRenderer()
        _wizard_result_file_renderer = WizardResultFileRenderer()
        _reg_config_wizard_result_transformer = DeploymentConfigWizardResultTransformer()
        _deployment_config_wizard = DeploymentConfigWizard(_reg_config_wizard_result_transformer,
                                                           _wizard_result_console_renderer,
                                                           _wizard_result_file_renderer)

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
            _deployment_config_wizard
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

        print(f"Domino CLI v{version} initialized.")
        print("-" * 30)

        return _cli

    @staticmethod
    def _assert_config_value(config_parameter: str) -> str:

        config_value = os.getenv(config_parameter)
        if config_value is None:
            raise Exception("Configuration parameter {0} is not specified".format(config_parameter))

        return config_value
