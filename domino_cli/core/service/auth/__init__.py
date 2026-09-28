import datetime
import json
from base64 import b64decode


def parse_token_expiration(token: str) -> datetime.datetime:
    """
    Parses the expiration time from a JWT token.

    :param token: The JWT token.
    :return: The expiration time as a datetime object.
    """
    jwt_payload = json.loads(b64decode(str(token).split(".")[1] + "=="))
    expires_at = datetime.datetime.fromtimestamp(jwt_payload["exp"])

    return expires_at
