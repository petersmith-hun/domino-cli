class SessionContext:
    """
    Domain class wrapping Domino CLI authenticated session data.
    """
    def __init__(self, username: str, authentication_token: str):
        self.username: str = username
        self.authentication_token: str = authentication_token
