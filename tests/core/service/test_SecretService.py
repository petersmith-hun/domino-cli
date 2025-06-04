import unittest
from unittest import mock
from unittest.mock import call

from requests import Response

from domino_cli.core.client.DominoClient import DominoClient
from domino_cli.core.domain.DominoRequest import DominoRequest
from domino_cli.core.domain.HTTPMethod import HTTPMethod
from domino_cli.core.service.SecretService import SecretService


class SecretServiceTest(unittest.TestCase):

    def setUp(self):
        self._domino_client_mock = mock.create_autospec(DominoClient)
        self._response_mock = mock.create_autospec(Response)
        self._secret_service = SecretService(self._domino_client_mock)

    @mock.patch("builtins.print", side_effect=print)
    def test_should_create_secret(self, print_mock):

        # given
        request_body = {
            "key": "config.test",
            "context": "ctx",
            "value": "new-secret-value",
        }

        expected_request = DominoRequest(
            method=HTTPMethod.POST,
            path="/secrets",
            body=request_body,
            authenticated=True
        )

        self._domino_client_mock.send_command.return_value = self._response_mock
        self._response_mock.status_code = 200

        # when
        self._secret_service.create_secret(request_body["key"], request_body["context"], request_body["value"])

        # then
        self._domino_client_mock.send_command.assert_called_with(expected_request)
        print_mock.assert_called_with("[info ] Operation finished successfully")

    @mock.patch("builtins.print", side_effect=print)
    def test_should_create_secret_return_with_validation_error(self, print_mock):

        # given
        request_body = {
            "key": "#bad??key",
            "context": "bad!!!context",
            "value": "new-secret-value",
        }

        expected_request = DominoRequest(
            method=HTTPMethod.POST,
            path="/secrets",
            body=request_body,
            authenticated=True
        )

        self._domino_client_mock.send_command.return_value = self._response_mock
        self._response_mock.json.return_value = {
            "message": "Validation error",
            "violations": [
                {"field": "key", "message": "Invalid key"},
                {"field": "context", "message": "Invalid context"},
            ]
        }
        self._response_mock.status_code = 400

        # when
        self._secret_service.create_secret(request_body["key"], request_body["context"], request_body["value"])

        # then
        self._domino_client_mock.send_command.assert_called_with(expected_request)
        print_mock.assert_has_calls([
            call("[error] Failed to execute operation, Domino responded with status 400: Validation error"),
            call("[error] Invalid field [key]: Invalid key"),
            call("[error] Invalid field [context]: Invalid context"),
        ])

    @mock.patch("builtins.print", side_effect=print)
    def test_should_create_secret_return_with_validation_error_and_handle_invalid_response(self, print_mock):

        # given
        request_body = {
            "key": "#bad??key",
            "context": "bad!!!context",
            "value": "new-secret-value",
        }

        expected_request = DominoRequest(
            method=HTTPMethod.POST,
            path="/secrets",
            body=request_body,
            authenticated=True
        )

        self._domino_client_mock.send_command.return_value = self._response_mock
        self._response_mock.json.return_value = None
        self._response_mock.text = "HTTP 400"
        self._response_mock.status_code = 400

        # when
        self._secret_service.create_secret(request_body["key"], request_body["context"], request_body["value"])

        # then
        self._domino_client_mock.send_command.assert_called_with(expected_request)
        print_mock.assert_called_with("[error] Failed to execute operation, Domino responded with status 400: HTTP 400")

    @mock.patch("builtins.print", side_effect=print)
    def test_should_get_all_metadata(self, print_mock):

        # given
        expected_request = DominoRequest(
            method=HTTPMethod.GET,
            path="/secrets",
            body=None,
            authenticated=True
        )

        self._domino_client_mock.send_command.return_value = self._response_mock
        self._response_mock.status_code = 201
        self._response_mock.content = "json-representation-of-the-response-below"
        self._response_mock.json.return_value = [
            {
                "context": "volumes",
                "secrets": [
                    {"key": "volume.vfs", "retrievable": True},
                    {"key": "volume.logs", "retrievable": False},
                ]
            },
            {
                "context": "config",
                "secrets": [
                    {"key": "config.test", "retrievable": True},
                ]
            }
        ]

        # when
        self._secret_service.get_all_metadata()

        # then
        self._domino_client_mock.send_command.assert_called_with(expected_request)
        print_mock.assert_has_calls([
            call("[info ] Secrets in context [volumes]"),
            call("[info ]                     volume.vfs: Retrievable"),
            call("[info ]                    volume.logs: Not retrievable"),
            call(),
            call("[info ] Secrets in context [config]"),
            call("[info ]                    config.test: Retrievable"),
            call()
        ])

    @mock.patch("builtins.print", side_effect=print)
    def test_should_get_metadata_by_key(self, print_mock):

        # given
        expected_request = DominoRequest(
            method=HTTPMethod.GET,
            path="/secrets/volume.vfs/metadata",
            body=None,
            authenticated=True
        )

        self._domino_client_mock.send_command.return_value = self._response_mock
        self._response_mock.status_code = 200
        self._response_mock.content = "json-representation-of-the-response-below"
        self._response_mock.json.return_value = {
            "key": "volume.vfs",
            "context": "config",
            "retrievable": True
        }

        # when
        self._secret_service.get_metadata_by_key("volume.vfs")

        # then
        self._domino_client_mock.send_command.assert_called_with(expected_request)
        print_mock.assert_has_calls([
            call("[info ]                            key: volume.vfs"),
            call("[info ]                        context: config"),
            call("[info ]                    retrievable: True")
        ])

    @mock.patch("builtins.print", side_effect=print)
    def test_should_get_metadata_by_key_handle_missing_secret(self, print_mock):

        # given
        expected_request = DominoRequest(
            method=HTTPMethod.GET,
            path="/secrets/missing.key/metadata",
            body=None,
            authenticated=True
        )

        self._domino_client_mock.send_command.return_value = self._response_mock
        self._response_mock.status_code = 404
        self._response_mock.content = "json-representation-of-the-response-below"
        self._response_mock.json.return_value = {
            "message": "Missing secret"
        }

        # when
        self._secret_service.get_metadata_by_key("missing.key")

        # then
        self._domino_client_mock.send_command.assert_called_with(expected_request)
        print_mock.assert_called_with("[error] Failed to execute operation, Domino responded with status 404: Missing secret")

    @mock.patch("builtins.print", side_effect=print)
    def test_should_retrieve_secret_by_key(self, print_mock):

        # given
        expected_request = DominoRequest(
            method=HTTPMethod.GET,
            path="/secrets/volume.logs",
            body=None,
            authenticated=True
        )

        self._domino_client_mock.send_command.return_value = self._response_mock
        self._response_mock.status_code = 200
        self._response_mock.content = "json-representation-of-the-response-below"
        self._response_mock.json.return_value = {
            "volume.logs": "/tmp/app/logs"
        }

        # when
        self._secret_service.retrieve_secret_by_key("volume.logs")

        # then
        self._domino_client_mock.send_command.assert_called_with(expected_request)
        print_mock.assert_called_with("[info ]                    volume.logs: /tmp/app/logs")

    @mock.patch("builtins.print", side_effect=print)
    def test_should_retrieve_secrets_by_context(self, print_mock):

        # given
        expected_request = DominoRequest(
            method=HTTPMethod.GET,
            path="/secrets/context/volumes",
            body=None,
            authenticated=True
        )

        self._domino_client_mock.send_command.return_value = self._response_mock
        self._response_mock.status_code = 200
        self._response_mock.content = "json-representation-of-the-response-below"
        self._response_mock.json.return_value = {
            "volume.logs": "/tmp/app/logs",
            "volume.vfs": "/tmp/vfs"
        }

        # when
        self._secret_service.retrieve_secrets_by_context("volumes")

        # then
        self._domino_client_mock.send_command.assert_called_with(expected_request)
        print_mock.assert_has_calls([
            call("[info ]                    volume.logs: /tmp/app/logs"),
            call("[info ]                     volume.vfs: /tmp/vfs")
        ])

    @mock.patch("builtins.print", side_effect=print)
    def test_should_lock_secret(self, print_mock):

        # given
        expected_request = DominoRequest(
            method=HTTPMethod.DELETE,
            path="/secrets/volume.vfs/retrieval",
            body=None,
            authenticated=True
        )

        self._domino_client_mock.send_command.return_value = self._response_mock
        self._response_mock.status_code = 204

        # when
        self._secret_service.lock_secret("volume.vfs")

        # then
        self._domino_client_mock.send_command.assert_called_with(expected_request)
        print_mock.assert_called_with("[info ] Operation finished successfully")

    @mock.patch("builtins.print", side_effect=print)
    def test_should_unlock_secret(self, print_mock):

        # given
        expected_request = DominoRequest(
            method=HTTPMethod.PUT,
            path="/secrets/volume.vfs/retrieval",
            body=None,
            authenticated=True
        )

        self._domino_client_mock.send_command.return_value = self._response_mock
        self._response_mock.status_code = 204

        # when
        self._secret_service.unlock_secret("volume.vfs")

        # then
        self._domino_client_mock.send_command.assert_called_with(expected_request)
        print_mock.assert_called_with("[info ] Operation finished successfully")

    @mock.patch("builtins.print", side_effect=print)
    def test_should_delete_secret(self, print_mock):

        # given
        expected_request = DominoRequest(
            method=HTTPMethod.DELETE,
            path="/secrets/volume.vfs",
            body=None,
            authenticated=True
        )

        self._domino_client_mock.send_command.return_value = self._response_mock
        self._response_mock.status_code = 204

        # when
        self._secret_service.delete_secret("volume.vfs")

        # then
        self._domino_client_mock.send_command.assert_called_with(expected_request)
        print_mock.assert_called_with("[info ] Operation finished successfully")

