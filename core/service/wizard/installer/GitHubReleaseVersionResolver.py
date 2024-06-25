import re

import requests

from core.service.wizard.installer import VersionResolver
from core.util.ArrayStream import ArrayStream
from installer_config import DominoComponent, installer_config


class GitHubReleaseVersionResolver(VersionResolver):
    """
    VersionHelper implementation to resolve GitHub Release tag versions.
    """

    def resolve_latest(self, component: DominoComponent) -> str:

        available_releases = requests.get(installer_config.github_release_version_source)

        release_name = ArrayStream(available_releases.json()) \
            .filter(lambda release: str(release["tag_name"]).startswith(component.value)) \
            .filter(lambda release: str(release["tag_name"]).endswith(".release")) \
            .sort(lambda release: release["created_at"]) \
            .last()["tag_name"]

        return re.search("^.*-v([0-9]+\.[0-9]+\.[0-9]+-[0-9]+)\.release$", release_name).group(1)
