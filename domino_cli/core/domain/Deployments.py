from typing import Any


class ResponseContainer[T]:
    def __init__(self):
        self.result: T | None = None

    def set_result(self, result: T):
        self.result = result

    def get_result(self) -> T:
        return self.result


class DeploymentSummary:

    def __init__(self, json_content: dict[str, Any]):
        self.id = json_content.get("id")
        self.source_type = json_content.get("sourceType")
        self.execution_type = json_content.get("executionType")
        self.home = json_content.get("home")
        self.resource = json_content.get("resource")
        self.locked = json_content.get("locked")
