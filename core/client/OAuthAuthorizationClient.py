import base64

import requests
from requests import Response

from core.domain.HTTPMethod import HTTPMethod
from core.domain.OAuthConfig import OAuthConfig

_ENCODING = "UTF-8"


class OAuthAuthorizationClient:
    """
    HTTP client implementation for sending requests to the configured OAuth Authorization Server.
    """
    def __init__(self, oauth_config: OAuthConfig):
        self._oauth_config = oauth_config

    def request_authorization(self) -> Response:
        """
        Requests an access token from the configured OAuth Authorization Server.
        Request is sent as Client Credentials Grant Flow token request, including the client ID and the scope,
        as well as the basic authorization header.

        :return: the response object
        """
        return requests.request(str(HTTPMethod.POST.value),
                                self._prepare_token_url(),
                                data=self._prepare_token_request_form(),
                                headers=self._prepare_token_request_headers())

    def _prepare_token_url(self) -> str:

        return self._oauth_config.token_url \
            if self._oauth_config.audience is None \
            else f"{self._oauth_config.token_url}?audience={self._oauth_config.audience}"

    def _prepare_token_request_form(self) -> dict[str, str]:

        return {
            "grant_type": "client_credentials",
            "client_id": self._oauth_config.client_id,
            "scope": self._oauth_config.scope
        }

    def _prepare_token_request_headers(self) -> dict[str, str]:

        credentials: str = f"{self._oauth_config.client_id}:{self._oauth_config.client_secret}"
        base64_encoded_credentials: str = base64.b64encode(bytes(credentials, _ENCODING)).decode(_ENCODING)
        auth_header_value: str = f"Basic {base64_encoded_credentials}"

        return {
            "Authorization": auth_header_value
        }
