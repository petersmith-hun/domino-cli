import requests

from domino_cli.core.service.wizard.installer import VersionResolver
from domino_cli.core.util.ArrayStream import ArrayStream
from domino_cli.installer_config import DominoComponent, installer_config


class DockerVersionResolver(VersionResolver):
    """
    VersionHelper implementation to resolve Docker tag versions.
    """
    def resolve_latest(self, component: DominoComponent) -> str:

        component_tags_path = installer_config.docker_version_source.replace("{component}", component.value)
        available_tags = requests.get(component_tags_path)

        latest_exact_tag = ArrayStream(available_tags.json()["results"]) \
            .filter(lambda tag: tag["name"] != "latest") \
            .sort(lambda tag: tag["last_updated"]) \
            .last()

        return "" \
            if latest_exact_tag is None \
            else latest_exact_tag["name"]
