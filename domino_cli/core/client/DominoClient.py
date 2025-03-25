import urllib.parse

import requests
from requests import Response

from domino_cli.core.cli.Logging import info
from domino_cli.core.domain.DominoRequest import DominoRequest
from domino_cli.core.service.SessionContextHolder import SessionContextHolder


class DominoClient:
    """
    HTTP client implementation for sending REST request to Domino.
    """
    def __init__(self, domino_base_url: str, session_context_holder: SessionContextHolder):
        self._domino_base_url = domino_base_url
        self._session_context_holder = session_context_holder

        info("Domino CLI is configured to communicate with Domino on {0}".format(domino_base_url))

    def send_command(self, domino_request: DominoRequest) -> Response:
        """
        Prepares and sends a REST request to Domino based on the given DominoRequest object.

        :param domino_request: DominoRequest object specifying request parameters
        :return: Response object
        """
        resolved_path = urllib.parse.urljoin(self._domino_base_url, domino_request.path)
        headers = {"Content-Type": "text/plain"} \
            if domino_request.as_text \
            else {"Content-Type": "application/json"}
        auth = self._session_context_holder.get_bearer_auth() if domino_request.authenticated else None

        if auth:
            headers.update(auth)

        return requests.request(domino_request.method.value, resolved_path, headers=headers,
                                json=None if domino_request.as_text else domino_request.body,
                                data=domino_request.body if domino_request.as_text else None)
