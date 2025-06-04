from requests import Response

from domino_cli.core.cli.Logging import info


def is_successful(response: Response) -> bool:
    """
    Checks if the given response is successful (i.e. the status is between 200 and 300).

    :param response: response to check
    :return: boolean true if the response is successful, false otherwise
    """
    return 200 <= response.status_code < 300

def render_response(response: Response) -> None:
    """
    Basic response rendering.

    :param response: response to render
    """
    if len(response.content) == 0:
        info("No further response received from Domino")
        print()
        return

    response_dict = response.json()
    info(" --- Response details ---")
    [info("{:>20}: {}".format(field, response_dict[field])) for field in response_dict]
    print()
