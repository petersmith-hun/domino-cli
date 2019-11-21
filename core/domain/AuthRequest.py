class AuthRequest:
    """
    Authentication request data domain class.
    """
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def get_as_dict(self) -> dict:
        """
        Returns the contents as dict (JSON-serializable).

        :return: contents as dict
        """
        return {
            "username": self.username,
            "password": self.password
        }
