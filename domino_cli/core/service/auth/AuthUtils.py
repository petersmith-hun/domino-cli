import os
from getpass import getpass

from domino_cli.core.cli.RuntimeHelper import RuntimeHelper

_DOMINO_CLI_USERNAME = "DOMINO_CLI_USERNAME"
_DOMINO_CLI_PASSWORD = "DOMINO_CLI_PASSWORD"


class AuthUtils:
    """
    Authentication process related static utility methods.
    """

    @staticmethod
    def input_username() -> str:
        """
        Tries to resolve the username from the DOMINO_CLI_USERNAME environment variable.
        If not present, prompts the user to specify it on the terminal.

        :return: resolved username
        """
        username = os.getenv(_DOMINO_CLI_USERNAME)
        if username is None:
            username = RuntimeHelper.input_wrapper(lambda: input(" ** specify username: "))

        return username

    @staticmethod
    def input_password() -> str:
        """
        Tries to resolve the password from the DOMINO_CLI_PASSWORD environment variable.
        If not present, prompts the user to specify it on the terminal (keeping it hidden while typing).

        :return: resolved password
        """
        password = os.getenv(_DOMINO_CLI_PASSWORD)
        if password is None:
            password = RuntimeHelper.input_wrapper(lambda: getpass(" ** specify password: "))

        return password
