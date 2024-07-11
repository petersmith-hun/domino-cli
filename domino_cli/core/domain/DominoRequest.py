from domino_cli.core.domain.HTTPMethod import HTTPMethod


class DominoRequest:
    """
    REST request parameter wrapper.
    """
    def __init__(self, method: HTTPMethod, path: str, body=None, authenticated: bool = False):
        self.method = method
        self.path = path
        self.body = body
        self.authenticated = authenticated

    def __repr__(self):
        return "[{0} {1}]".format(self.method.value, self.path)
