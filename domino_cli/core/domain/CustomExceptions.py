from requests import Response


class AuthenticationException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class DominoServiceException(Exception):
    def __init__(self, response: Response):
        response_data = response.json() if len(response.text) > 0 else {}
        super().__init__(response_data.get("message", "Domino failed to process request"))
        self.status_code = response.status_code


class ViolationsModel:

    class Violation:
        def __init__(self, violation: dict):
            self.field = violation.get("field")
            self.message = violation.get("message")

    def __init__(self, response: Response):
        response_data = response.json()
        self.violations = [self.Violation(violation) for violation in response_data.get("violations", [])] \
            if response_data \
            else []


class ValidationException(Exception):
    def __init__(self, response: Response):
        super().__init__("Validation error")
        self.violations = ViolationsModel(response)
