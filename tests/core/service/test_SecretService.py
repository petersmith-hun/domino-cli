import json
import unittest
from unittest import mock

from requests import Response

from domino_cli.core.client.DominoClient import DominoClient
from domino_cli.core.domain.CustomExceptions import ValidationException, DominoServiceException
from domino_cli.core.domain.DominoRequest import DominoRequest
from domino_cli.core.domain.HTTPMethod import HTTPMethod
from domino_cli.core.domain.Secrets import SecretGroup, SecretDetails
from domino_cli.core.service.SecretService import SecretService
from domino_cli.core.service.utility.APIRequestHandler import APIRequestHandler


class SecretServiceTest(unittest.TestCase):

    def setUp(self):
        self._domino_client_mock = mock.create_autospec(DominoClient)
        self._api_request_handler = APIRequestHandler(self._domino_client_mock)
        self._response_mock = mock.create_autospec(Response)
        self._secret_service = SecretService(self._api_request_handler)

    def test_should_create_secret(self):

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

    def test_should_create_secret_return_with_validation_error(self):

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
        throwing = lambda: self._secret_service.create_secret(request_body["key"], request_body["context"], request_body["value"])

        # then
        self.assertRaises(ValidationException, throwing)
        self._domino_client_mock.send_command.assert_called_with(expected_request)

    def test_should_create_secret_return_with_validation_error_and_handle_invalid_response(self):

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
        throwing = lambda: self._secret_service.create_secret(request_body["key"], request_body["context"], request_body["value"])

        # then
        self.assertRaises(ValidationException, throwing)
        self._domino_client_mock.send_command.assert_called_with(expected_request)

    def test_should_get_all_metadata(self):

        # given
        expected_request = DominoRequest(
            method=HTTPMethod.GET,
            path="/secrets",
            body=None,
            authenticated=True
        )

        expected_result = [
            SecretGroup({
                "context": "volumes",
                "secrets": [
                    {"key": "volume.vfs", "retrievable": True},
                    {"key": "volume.logs", "retrievable": False},
                ]
            }),
            SecretGroup({
                "context": "config",
                "secrets": [
                    {"key": "config.test", "retrievable": True},
                ]
            })
        ]

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
        result = self._secret_service.get_all_metadata()

        # then
        self._domino_client_mock.send_command.assert_called_with(expected_request)
        self.assertEqual(json.dumps(result, default=lambda obj: obj.__dict__), json.dumps(expected_result, default=lambda obj: obj.__dict__))

    def test_should_get_metadata_by_key(self):

        # given
        expected_request = DominoRequest(
            method=HTTPMethod.GET,
            path="/secrets/volume.vfs/metadata",
            body=None,
            authenticated=True
        )

        expected_result = SecretDetails({
            "key": "volume.vfs",
            "context": "config",
            "retrievable": True
        })

        self._domino_client_mock.send_command.return_value = self._response_mock
        self._response_mock.status_code = 200
        self._response_mock.content = "json-representation-of-the-response-below"
        self._response_mock.json.return_value = {
            "key": "volume.vfs",
            "context": "config",
            "retrievable": True
        }

        # when
        result = self._secret_service.get_metadata_by_key("volume.vfs")

        # then
        self._domino_client_mock.send_command.assert_called_with(expected_request)
        self.assertEqual(json.dumps(result, default=lambda obj: obj.__dict__), json.dumps(expected_result, default=lambda obj: obj.__dict__))

    def test_should_get_metadata_by_key_handle_missing_secret(self):

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
        throwing = lambda: self._secret_service.get_metadata_by_key("missing.key")

        # then
        self.assertRaises(DominoServiceException, throwing)
        self._domino_client_mock.send_command.assert_called_with(expected_request)

    def test_should_retrieve_secret_by_key(self):

        # given
        expected_request = DominoRequest(
            method=HTTPMethod.GET,
            path="/secrets/volume.logs",
            body=None,
            authenticated=True
        )

        expected_result = {
            "volume.logs": "/tmp/app/logs"
        }

        self._domino_client_mock.send_command.return_value = self._response_mock
        self._response_mock.status_code = 200
        self._response_mock.content = "json-representation-of-the-response-below"
        self._response_mock.json.return_value = expected_result

        # when
        result = self._secret_service.retrieve_secret_by_key("volume.logs")

        # then
        self._domino_client_mock.send_command.assert_called_with(expected_request)
        self.assertEqual(result, expected_result)

    def test_should_retrieve_secrets_by_context(self):

        # given
        expected_request = DominoRequest(
            method=HTTPMethod.GET,
            path="/secrets/context/volumes",
            body=None,
            authenticated=True
        )

        expected_result = {
            "volume.logs": "/tmp/app/logs",
            "volume.vfs": "/tmp/vfs"
        }

        self._domino_client_mock.send_command.return_value = self._response_mock
        self._response_mock.status_code = 200
        self._response_mock.content = "json-representation-of-the-response-below"
        self._response_mock.json.return_value = expected_result

        # when
        result = self._secret_service.retrieve_secrets_by_context("volumes")

        # then
        self._domino_client_mock.send_command.assert_called_with(expected_request)
        self.assertEqual(result, expected_result)

    def test_should_lock_secret(self):

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

    def test_should_unlock_secret(self):

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

    def test_should_delete_secret(self):

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

