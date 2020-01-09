import os

from core.cli.CLI import CLI
from core.client.DominoClient import DominoClient
from core.command.AuthCommand import AuthCommand
from core.command.DeployApplicationCommand import DeployApplicationCommand
from core.command.ExitCommand import ExitCommand
from core.command.HelpCommand import HelpCommand
from core.command.RestartApplicationCommand import RestartApplicationCommand
from core.command.StartApplicationCommand import StartApplicationCommand
from core.command.StopApplicationCommand import StopApplicationCommand
from core.command.WizardCommand import WizardCommand
from core.service.AuthenticationService import AuthenticationService
from core.service.CommandProcessor import CommandProcessor
from core.service.ConfigurationWizardService import ConfigurationWizardService
from core.service.DominoService import DominoService
from core.service.SessionContextHolder import SessionContextHolder
from core.service.wizard.RegistrationConfigWizard import RegistrationConfigWizard


class ApplicationContext:
    """
    Simple IoC container for Domino CLI.
    """
    @staticmethod
    def init_cli() -> CLI:

        print("Initializing Domino CLI...")

        # configuration properties
        _domino_base_url = ApplicationContext._assert_config_value("DOMINO_BASE_URL")

        # wizards
        _registration_config_wizard = RegistrationConfigWizard()

        # common components
        _session_context_holder = SessionContextHolder()
        _domino_client = DominoClient(_domino_base_url, _session_context_holder)
        _domino_service = DominoService(_domino_client)
        _auth_service = AuthenticationService(_domino_client, _session_context_holder)
        _config_wizard_service = ConfigurationWizardService([
            _registration_config_wizard
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

        # command processor
        _command_processor = CommandProcessor(_command_help, [
            _command_help,
            _command_exit,
            _command_auth,
            _command_deploy_app,
            _command_restart_app,
            _command_start_app,
            _command_stop_app,
            _command_wizard
        ])

        _cli = CLI(_command_processor)

        print("Domino CLI initialized.")
        print("-" * 30)

        return _cli

    @staticmethod
    def _assert_config_value(config_parameter: str) -> str:

        config_value = os.getenv(config_parameter)
        if config_value is None:
            raise Exception("Configuration parameter {0} is not specified".format(config_parameter))

        return config_value
