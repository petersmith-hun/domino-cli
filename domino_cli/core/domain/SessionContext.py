import datetime


class SessionContext:
    """
    Domain class wrapping Domino CLI authenticated session data.
    """
    def __init__(self, username: str, authentication_token: str, expires_at: datetime.datetime):
        self.username: str = username
        self.authentication_token: str = authentication_token
        self.expires_at: datetime.datetime = expires_at
