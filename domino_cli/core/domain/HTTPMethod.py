from enum import Enum


class HTTPMethod(Enum):
    """
    Enum class specifying the possible HTTP methods.
    """

    POST = "POST"
    PUT = "PUT"
    GET = "GET"
    DELETE = "DELETE"
