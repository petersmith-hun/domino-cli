from domino_cli.core.cli.RuntimeHelper import RuntimeHelper
from domino_cli.core.command.AbstractCommand import AbstractCommand
from domino_cli.core.domain.CommandDescriptor import CommandDescriptor

_COMMAND_NAME = "help"
_HELP_CONTENT = """
Known commands:
 - exit: exits CLI (requires no arguments)
 - help: shows this help (requires no arguments)
 - auth <flag>: authentication utilities
    Flags can be:
    --encrypt-password: encrypts the given password for usage in Domino
    --generate-token: authenticates with Domino and prints the generated token
    --open-session: authenticates with Domino and stores the token in the session context for further usage
    --set-mode <oauth|direct>: switches authentication mode (oauth or direct)
 - secret <arguments>: secret management operations
    --metadata --all: retrieves metadata of all existing secrets
    --metadata <key>: retrieves metadata of the given secret
    --retrieve --key <key>: retrieves the value of the given secret
    --retrieve --context <context>: retrieves the value of all secrets under the given context
    --create <key> <context>: create a new secret (you'll be prompted to enter the secret value as password)
    --lock <key>: locks a secret (disables retrieval)
    --unlock <key>: unlocks a secret (enables retrieval)
    --delete <key>: deletes a secret 
 - start <app>: commands Domino to start the given app
 - stop <app>: commands Domino to stop the given app
 - restart <app>: commands Domino to restart the given app
 - deploy <app> <latest|version>: commands Domino to deploy either the latest or the specified version of the given app
 - wizard <wizard name>: starts the specified configuration wizard
 """


class HelpCommand(AbstractCommand):
    """
    Prints help contents, containing information about the supported commands.
    """
    def __init__(self):
        super().__init__(_COMMAND_NAME)
        self._help_text = _HELP_CONTENT.splitlines(keepends=True)

    def execute_command(self, command_descriptor: CommandDescriptor) -> None:
        [print(line, end="") for line in self._help_text]
        RuntimeHelper.exit_with_error_in_cicd_mode()
