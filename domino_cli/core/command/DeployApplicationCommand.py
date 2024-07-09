from domino_cli.core.command.AbstractCommand import AbstractCommand
from domino_cli.core.domain.CommandDescriptor import CommandDescriptor
from domino_cli.core.domain.DominoCommand import DominoCommand
from domino_cli.core.service.DominoService import DominoService

_LATEST_KEYWORD = "latest"
_COMMAND_NAME = "deploy"


class DeployApplicationCommand(AbstractCommand):
    """
    Lifecycle command implementation being able to send a deploy command for the given application.
    """
    def __init__(self, domino_service: DominoService):
        super().__init__(_COMMAND_NAME)
        self._domino_service = domino_service

    def execute_command(self, command_descriptor: CommandDescriptor) -> None:
        """
        Sends a deployment command for the given application.
        Argument array must contain two parameters:
         - application name
         - "latest" keyword or an explicit version of the application to be deployed

        :param command_descriptor: CommandDescriptor object containing the command arguments
        """
        if not len(command_descriptor.arguments) == 2:
            print("Application name and 'latest' keyword or explicit version is required")
        else:
            application: str = command_descriptor.arguments[0]
            version: str = command_descriptor.arguments[1]
            command: DominoCommand = DominoCommand.DEPLOY_LATEST \
                if version == _LATEST_KEYWORD \
                else DominoCommand.DEPLOY_VERSION

            self._domino_service.execute_lifecycle_command(command, application, version)
