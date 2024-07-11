import re

import requests

from domino_cli.core.service.wizard.installer import VersionResolver
from domino_cli.core.util.ArrayStream import ArrayStream
from domino_cli.installer_config import DominoComponent, installer_config


class GitHubReleaseVersionResolver(VersionResolver):
    """
    VersionHelper implementation to resolve GitHub Release tag versions.
    """

    def resolve_latest(self, component: DominoComponent) -> str:

        available_releases = requests.get(installer_config.github_release_version_source)

        latest_release_name = ArrayStream(available_releases.json()) \
            .filter(lambda release: str(release["tag_name"]).startswith(component.value)) \
            .filter(lambda release: str(release["tag_name"]).endswith(".release")) \
            .sort(lambda release: release["created_at"]) \
            .last()

        return "" \
            if latest_release_name is None \
            else self._extract_version(latest_release_name)

    @staticmethod
    def _extract_version(release: dict) -> str:

        match = re.search("^.*-v([0-9]+\\.[0-9]+\\.[0-9]+-[0-9]+)\\.release$", release["tag_name"])

        return "" \
            if match is None \
            else match.group(1)
