from enum import Enum

from core.domain.HTTPMethod import HTTPMethod


class DominoRequestDescriptor:
    """
    Command descriptor for Domino commands, specifying the expected HTTP method and a request path template.
    """
    def __init__(self, method: HTTPMethod, path_template: str):
        self.method = method
        self.path_template = path_template


class DominoCommand(Enum):
    """
    Enum of possible Domino commands.
    Each enum value must specify its own DominoRequestDescriptor instance.
    """

    START = DominoRequestDescriptor(HTTPMethod.PUT, "/lifecycle/{0}/start")
    STOP = DominoRequestDescriptor(HTTPMethod.DELETE, "/lifecycle/{0}/stop")
    RESTART = DominoRequestDescriptor(HTTPMethod.PUT, "/lifecycle/{0}/restart")
    DEPLOY_LATEST = DominoRequestDescriptor(HTTPMethod.PUT, "/lifecycle/{0}/deploy")
    DEPLOY_VERSION = DominoRequestDescriptor(HTTPMethod.PUT, "/lifecycle/{0}/deploy/{1}")
    INFO = DominoRequestDescriptor(HTTPMethod.GET, "/lifecycle/{0}/info")
