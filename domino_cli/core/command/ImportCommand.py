from domino_cli.core.cli.Logging import error
from domino_cli.core.cli.RuntimeHelper import RuntimeHelper
from domino_cli.core.command.AbstractCommand import AbstractCommand
from domino_cli.core.domain.CommandDescriptor import CommandDescriptor
from domino_cli.core.service.DominoService import DominoService

_COMMAND_NAME = "import"


class ImportCommand(AbstractCommand):
    """
    Command implementation to import a deployment definition from static YAML configuration file.
    """
    def __init__(self, domino_service: DominoService):
        super().__init__(_COMMAND_NAME)
        self._domino_service = domino_service

    def execute_command(self, command_descriptor: CommandDescriptor) -> None:

        if len(command_descriptor.arguments) > 1:
            error("Too many arguments, expected command usage is 'import optional/path/to/deployment.yml' (defaults to '.domino/deployment.yml' without argument)")
            RuntimeHelper.exit_with_error_in_cicd_mode()
            return

        definition_path = command_descriptor.arguments[0] \
            if len(command_descriptor.arguments) == 1 \
            else None

        self._domino_service.import_definition(definition_path)
