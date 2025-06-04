from enum import Enum

from domino_cli.core.domain.HTTPMethod import HTTPMethod


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
    IMPORT = DominoRequestDescriptor(HTTPMethod.POST, "/deployments/import")

    RETRIEVE_ALL_METADATA = DominoRequestDescriptor(HTTPMethod.GET, "/secrets")
    RETRIEVE_SECRET = DominoRequestDescriptor(HTTPMethod.GET, "/secrets/{0}")
    RETRIEVE_SECRET_METADATA = DominoRequestDescriptor(HTTPMethod.GET, "/secrets/{0}/metadata")
    RETRIEVE_SECRETS_BY_CONTEXT = DominoRequestDescriptor(HTTPMethod.GET, "/secrets/context/{0}")
    CREATE_SECRET = DominoRequestDescriptor(HTTPMethod.POST, "/secrets")
    LOCK_SECRET = DominoRequestDescriptor(HTTPMethod.DELETE, "/secrets/{0}/retrieval")
    UNLOCK_SECRET = DominoRequestDescriptor(HTTPMethod.PUT, "/secrets/{0}/retrieval")
    DELETE_SECRET = DominoRequestDescriptor(HTTPMethod.DELETE, "/secrets/{0}")
