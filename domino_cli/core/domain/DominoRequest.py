from domino_cli.core.domain.HTTPMethod import HTTPMethod


class DominoRequest:
    """
    REST request parameter wrapper.
    """
    def __init__(self, method: HTTPMethod, path: str, body=None, as_text: bool = False, authenticated: bool = False):
        self.method = method
        self.path = path
        self.body = body
        self.as_text = as_text
        self.authenticated = authenticated

    def __repr__(self):
        return "[{0} {1}]".format(self.method.value, self.path)
