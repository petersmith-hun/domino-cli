from __future__ import annotations

from enum import Enum


class AuthMode(Enum):
    """
    Supported modes for authenticating with Domino.
    """
    DIRECT = "direct"
    OAUTH = "oauth"

    @staticmethod
    def by_value(auth_mode: str) -> AuthMode:
        """
        Parses auth mode.
        Converts the given auth mode parameter to uppercase, before trying to convert it by name.

        :param auth_mode: auth mode value
        :return: parsed AuthMode
        :raise KeyError in case the given auth mode is unsupported
        """
        return AuthMode[auth_mode.upper()]
