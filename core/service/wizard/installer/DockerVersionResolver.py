import requests

from core.service.wizard.installer import VersionResolver
from core.util.ArrayStream import ArrayStream
from installer_config import DominoComponent, installer_config


class DockerVersionResolver(VersionResolver):
    """
    VersionHelper implementation to resolve Docker tag versions.
    """
    def resolve_latest(self, component: DominoComponent) -> str:

        component_tags_path = installer_config.docker_version_source.replace("{component}", component.value)
        available_tags = requests.get(component_tags_path)

        return ArrayStream(available_tags.json()["results"]) \
            .filter(lambda tag: tag["name"] != "latest") \
            .sort(lambda tag: tag["last_updated"]) \
            .last()["name"]
