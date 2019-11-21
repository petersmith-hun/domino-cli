from core.command.AbstractCommand import AbstractCommand
from core.domain.CommandDescriptor import CommandDescriptor
from core.service.AuthenticationService import AuthenticationService

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
        if not len(command_descriptor.arguments) == 1:
            AuthCommand._show_help()
        else:
            self._route_auth_request(command_descriptor.arguments[0])

    def _route_auth_request(self, operation_flag: str):

        if operation_flag == "--encrypt-password":
            self._authentication_service.encrypt_password()
        elif operation_flag == "--generate-token":
            self._authentication_service.generate_token()
        elif operation_flag == "--open-session":
            self._authentication_service.open_session()
        else:
            AuthCommand._show_help()

    @staticmethod
    def _show_help():
        print("Auth command requires operation flag of: --encrypt-password | --generate-token | --open-session")
