from domino_cli.core.cli.Logging import warning, error, info
from domino_cli.core.cli.RuntimeHelper import RuntimeHelper
from domino_cli.core.command.AbstractCommand import AbstractCommand
from domino_cli.core.domain.CommandDescriptor import CommandDescriptor
from domino_cli.core.domain.CustomExceptions import AuthenticationException
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
            additional_parameter: str | None = command_descriptor.arguments[1] \
                if len(command_descriptor.arguments) == 2 \
                else None
            self._route_auth_request(command_descriptor.arguments[0], additional_parameter)

    def _route_auth_request(self, operation_flag: str, additional_parameter: str | None):

        try:
            if operation_flag == "--encrypt-password":
                encrypted_password = self._authentication_service.encrypt_password()
                info("Encrypted password: {0}".format(encrypted_password))

            elif operation_flag == "--generate-token":
                access_token = self._authentication_service.generate_token()
                if RuntimeHelper.is_cicd_mode():
                    print(access_token)
                else:
                    info("Generated auth token: {0}".format(access_token))

            elif operation_flag == "--open-session":
                self._authentication_service.open_session()
                info("Session is open")

            elif operation_flag == "--set-mode" and additional_parameter is not None:
                self._authentication_service.set_mode(additional_parameter)

            else:
                AuthCommand._show_help()

        except AuthenticationException as exc:
            error(str(exc))
            RuntimeHelper.exit_with_error_in_cicd_mode()

    @staticmethod
    def _show_help():
        warning("Auth command requires operation flag of: --encrypt-password | --generate-token | --open-session "
              "| --set-mode direct|oauth")
