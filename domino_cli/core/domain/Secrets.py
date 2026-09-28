from typing import Any, cast


class SecretDetails:

    def __init__(self, json_content: dict[str, Any]):
        self.key = json_content.get("key")
        self.value = json_content.get("value")
        self.context = json_content.get("context")
        self.retrievable = json_content.get("retrievable")
        self.last_accessed_by = json_content.get("lastAccessedBy")
        self.last_accessed_at = json_content.get("lastAccessedAt")
        self.created_at = json_content.get("createdAt")
        self.updated_at = json_content.get("updatedAt")


class SecretGroup:

     def __init__(self, json_content: dict[str, Any]):
         self.context = json_content.get("context")
         self.secrets = [SecretDetails(secret) for secret in cast(list[dict[str, Any]], json_content.get("secrets"))]

