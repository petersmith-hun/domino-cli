from typing import List

from domino_cli.core.cli.Logging import error
from domino_cli.core.command.AbstractCommand import AbstractCommand
from domino_cli.core.command.dsl.dsm.DSLMain import SecretCommandProcessor
from domino_cli.core.domain.CommandDescriptor import CommandDescriptor

_command_processing_max_iteration = 4

_COMMAND_NAME = "secret"


class SecretCommand(AbstractCommand):
    """
    Command implementation to execute a Domino Secret Manager request.
    """
    def __init__(self, processors: List[SecretCommandProcessor]):
        super().__init__(_COMMAND_NAME)
        self._processors = {processor.for_subcommand(): processor for processor in processors}

    def execute_command(self, command_descriptor: CommandDescriptor) -> None:

        command_arguments = command_descriptor.arguments.copy()
        current_argument = "secret"
        processed = False

        for _ in range(_command_processing_max_iteration):

            processor = self._processors.get(current_argument)
            processed = processor.process(command_arguments)

            if processed:
                break

            current_argument = processor.chain_to(command_arguments)

            if current_argument is None:
                break

        if not processed:
            error("Domino CLI was not able to process your secret management request")
