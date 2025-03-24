from domino_cli.core.cli.Logging import warning
from domino_cli.core.command.AbstractCommand import AbstractCommand
from domino_cli.core.domain.CommandDescriptor import CommandDescriptor
from domino_cli.core.service.AuthenticationService import AuthenticationService

_COMMAND_NAME = "auth"


class AuthCommand(AbstractCommand):
    """
    Command implementation for authentication related operations.
    """
    def __init__(self, authentication_service: AuthenticationService):
        super().__init__(_COMMAND_NAME)
        self._authentication_service = authentication_service

    def execute_command(self, command_descriptor: CommandDescriptor) -> None:
        """
        Routes authentication command processing to the proper handler.

        :param command_descriptor: CommandDescriptor object containing the command arguments
        """
        if not 0 < len(command_descriptor.arguments) < 3:
            AuthCommand._show_help()
        else:
            additional_parameter: str = command_descriptor.arguments[1] \
                if len(command_descriptor.arguments) == 2 \
                else None
            self._route_auth_request(command_descriptor.arguments[0], additional_parameter)

    def _route_auth_request(self, operation_flag: str, additional_parameter: str):

        if operation_flag == "--encrypt-password":
            self._authentication_service.encrypt_password()
        elif operation_flag == "--generate-token":
            self._authentication_service.generate_token()
        elif operation_flag == "--open-session":
            self._authentication_service.open_session()
        elif operation_flag == "--set-mode":
            self._authentication_service.set_mode(additional_parameter)
        else:
            AuthCommand._show_help()

    @staticmethod
    def _show_help():
        warning("Auth command requires operation flag of: --encrypt-password | --generate-token | --open-session "
              "| --set-mode direct|oauth")
