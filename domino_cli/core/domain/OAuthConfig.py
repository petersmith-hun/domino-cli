import os

from domino_cli.core.cli.Logging import warning

_OAUTH_TOKEN_URL = "DOMINO_OAUTH_TOKEN_URL"
_OAUTH_CLIENT_ID = "DOMINO_OAUTH_CLIENT_ID"
_OAUTH_CLIENT_SECRET = "DOMINO_OAUTH_CLIENT_SECRET"
_OAUTH_SCOPE = "DOMINO_OAUTH_SCOPE"
_OAUTH_AUDIENCE = "DOMINO_OAUTH_AUDIENCE"


class OAuthConfig:
    """
    Domain class for holding OAuth configuration parameters.
    See README.md documentation for supported and required parameters.
    """
    def __init__(self):
        self.token_url = self._get_parameter(_OAUTH_TOKEN_URL)
        self.client_id = self._get_parameter(_OAUTH_CLIENT_ID)
        self.client_secret = self._get_parameter(_OAUTH_CLIENT_SECRET)
        self.scope = self._get_parameter(_OAUTH_SCOPE)
        self.audience = self._get_parameter(_OAUTH_AUDIENCE)

    def is_configured(self) -> bool:
        """
        Checks if all the necessary parameters are specified (audience is not mandatory, all the others are).

        :return: true if all the necessary parameters are specified, false otherwise
        """
        return all([
            self._verify_parameter(_OAUTH_TOKEN_URL),
            self._verify_parameter(_OAUTH_CLIENT_ID),
            self._verify_parameter(_OAUTH_CLIENT_SECRET),
            self._verify_parameter(_OAUTH_SCOPE)
        ])

    @staticmethod
    def _verify_parameter(parameter: str) -> bool:

        present: bool = True
        if OAuthConfig._get_parameter(parameter) is None:
            present = False
            warning(f"Parameter {parameter} is missing")

        return present

    @staticmethod
    def _get_parameter(parameter: str) -> str:
        return os.getenv(parameter)
