import unittest
from unittest import mock

from requests import Response

from domino_cli.core.service.wizard.installer.DockerVersionResolver import DockerVersionResolver
from domino_cli.installer_config import DominoComponent


class DockerVersionResolverTest(unittest.TestCase):

    def setUp(self) -> None:
        self.docker_version_resolver: DockerVersionResolver = DockerVersionResolver()
        self.response_mock: Response = mock.create_autospec(Response)

    @mock.patch("requests.get")
    def test_should_resolve_latest_for_coordinator(self, requests_get_mock):

        # given
        tags_response = {
            "results": [
                {"name": "latest", "last_updated": 3},
                {"name": "1.5", "last_updated": 2},
                {"name": "2.0", "last_updated": 3},
                {"name": "1.0", "last_updated": 1}
            ]
        }

        requests_get_mock.return_value = self.response_mock
        self.response_mock.json.return_value = tags_response

        # when
        result = self.docker_version_resolver.resolve_latest(DominoComponent.COORDINATOR)

        # then
        self.assertEqual(result, "2.0")
        requests_get_mock.assert_called_with("https://hub.docker.com/v2/namespaces/psproghu/repositories/domino-coordinator/tags")

    @mock.patch("requests.get")
    def test_should_resolve_latest_for_docker_agent(self, requests_get_mock):

        # given
        tags_response = {
            "results": [
                {"name": "latest", "last_updated": 10},
                {"name": "1.0", "last_updated": 1}
            ]
        }

        requests_get_mock.return_value = self.response_mock
        self.response_mock.json.return_value = tags_response

        # when
        result = self.docker_version_resolver.resolve_latest(DominoComponent.DOCKER_AGENT)

        # then
        self.assertEqual(result, "1.0")
        requests_get_mock.assert_called_with("https://hub.docker.com/v2/namespaces/psproghu/repositories/domino-docker-agent/tags")

    @mock.patch("requests.get")
    def test_should_resolve_latest_return_empty_string_for_missing_exact_version(self, requests_get_mock):

        # given
        tags_response = {
            "results": [
                {"name": "latest", "last_updated": 2}
            ]
        }

        requests_get_mock.return_value = self.response_mock
        self.response_mock.json.return_value = tags_response

        # when
        result = self.docker_version_resolver.resolve_latest(DominoComponent.DOCKER_AGENT)

        # then
        self.assertEqual(result, "")


if __name__ == "__main__":
    unittest.main()
