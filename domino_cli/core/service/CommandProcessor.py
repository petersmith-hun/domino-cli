import os
from typing import List

from domino_cli.core.cli.Logging import info
from domino_cli.core.command.AbstractCommand import AbstractCommand
from domino_cli.core.command.ExitCommand import ExitCommand
from domino_cli.core.domain.CommandDescriptor import CommandDescriptor

_DEBUG_MODE: bool = os.getenv("DOMINO_CLI_DEBUG_MODE", False)


class CommandProcessor:
    """
    Provides ability to process and execute CLI commands.
    """

    def __init__(self, default_command: AbstractCommand, commands: List[AbstractCommand]):
        self._default_command = default_command
        self._registered_commands = commands
        self._exit_command_class = ExitCommand

    def execute_command(self, command_descriptor: CommandDescriptor) -> bool:
        """
        Executes the given command provided as a CommandDescriptor object.

        :param command_descriptor: command and its arguments to be executed
        :return: boolean, true if CLI loop can be continued, false otherwise (exit command is called)
        """

        if _DEBUG_MODE:
            info("Command to be executed: {0}".format(command_descriptor))

        command_iterator = filter(lambda command: command.is_applicable(command_descriptor), self._registered_commands)
        selected_command = next(command_iterator, self._default_command)
        selected_command.execute_command(command_descriptor)

        return not isinstance(selected_command, self._exit_command_class)
