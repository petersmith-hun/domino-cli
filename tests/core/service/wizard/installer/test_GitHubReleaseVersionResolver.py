import unittest
from unittest import mock

from requests import Response

from domino_cli.core.service.wizard.installer.GitHubReleaseVersionResolver import GitHubReleaseVersionResolver
from domino_cli.installer_config import DominoComponent


class GitHubReleaseVersionResolverTest(unittest.TestCase):

    def setUp(self) -> None:
        self.github_release_version_resolver: GitHubReleaseVersionResolver = GitHubReleaseVersionResolver()
        self.response_mock: Response = mock.create_autospec(Response)

    @mock.patch("requests.get")
    def test_should_resolve_latest_for_bin_exec_agent(self, requests_get_mock):

        # given
        tags_response = [
            {"tag_name": "latest", "created_at": 3},
            {"tag_name": "coordinator-v1.5.0-6.release", "created_at": 6},
            {"tag_name": "binary-executable-agent-v1.3.0-5.release", "created_at": 3},
            {"tag_name": "binary-executable-agent-v1.2.0-4.release", "created_at": 2},
            {"tag_name": "1.0", "created_at": 4},
            {"tag_name": "binary-executable-agent-v1.4.0.rc.1", "created_at": 5},
        ]

        requests_get_mock.return_value = self.response_mock
        self.response_mock.json.return_value = tags_response

        # when
        result = self.github_release_version_resolver.resolve_latest(DominoComponent.BIN_EXEC_AGENT)

        # then
        self.assertEqual(result, "1.3.0-5")
        requests_get_mock.assert_called_with("https://api.github.com/repos/petersmith-hun/domino-platform/releases")

    @mock.patch("requests.get")
    def test_should_resolve_latest_return_empty_string_for_missing_exact_version(self, requests_get_mock):

        # given
        tags_response = [
            {"tag_name": "latest", "created_at": 2}
        ]

        requests_get_mock.return_value = self.response_mock
        self.response_mock.json.return_value = tags_response

        # when
        result = self.github_release_version_resolver.resolve_latest(DominoComponent.DOCKER_AGENT)

        # then
        self.assertEqual(result, "")


if __name__ == "__main__":
    unittest.main()
