from domino_cli.core.cli.Logging import error
from domino_cli.core.cli.RuntimeHelper import RuntimeHelper
from domino_cli.core.command.AbstractCommand import AbstractCommand
from domino_cli.core.domain.CommandDescriptor import CommandDescriptor
from domino_cli.core.service.DominoService import DominoService

_COMMAND_NAME = "oauth-import"


class OAuthImportCommand(AbstractCommand):
    """
    Command implementation to import an OAuth application descriptor from static YAML configuration file.
    """
    def __init__(self, domino_service: DominoService):
        super().__init__(_COMMAND_NAME)
        self._domino_service = domino_service

    def execute_command(self, command_descriptor: CommandDescriptor) -> None:

        argument_count = len(command_descriptor.arguments)
        if argument_count < 1 or argument_count > 3:
            error("Invalid arguments, expected command usage is 'oauth-import <deploymentID> [--dry-run] [optional/path/to/oauth.yml]' (defaults to '.domino/oauth.yml' without argument)")
            error("The optional --dry-run switch causes the descriptor to be verified only, without actually registering the application")
            RuntimeHelper.exit_with_error_in_cicd_mode()
            return

        application = command_descriptor.arguments[0]
        dry_run = "--dry-run" in command_descriptor.arguments
        descriptor_path = None

        if dry_run and len(command_descriptor.arguments) == 3:
            descriptor_path = command_descriptor.arguments[2]
        elif not dry_run and len(command_descriptor.arguments) == 2:
            descriptor_path = command_descriptor.arguments[1]

        self._domino_service.import_oauth_descriptor(application, dry_run, descriptor_path)
