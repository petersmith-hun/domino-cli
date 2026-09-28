import unittest
from unittest import mock

from requests import Response

from domino_cli.core.client.DominoClient import DominoClient
from domino_cli.core.domain.CustomExceptions import DominoServiceException
from domino_cli.core.domain.Deployments import LifecycleResponse
from domino_cli.core.domain.DominoCommand import DominoCommand
from domino_cli.core.domain.DominoRequest import DominoRequest
from domino_cli.core.domain.HTTPMethod import HTTPMethod
from domino_cli.core.service.DominoService import DominoService
from domino_cli.core.service.utility.APIRequestHandler import APIRequestHandler

_TEXT_DATA = "domino:\n\tdeployments:\n\t\tleaflet\n"


class DominoServiceTest(unittest.TestCase):

    def setUp(self) -> None:
        self.domino_client_mock: DominoClient = mock.create_autospec(DominoClient)
        self.api_request_handler_mock = mock.create_autospec(APIRequestHandler)
        self.domino_service: DominoService = DominoService(self.domino_client_mock, self.api_request_handler_mock)

    def test_should_execute_lifecycle_command_with_success(self):

        # given
        query = {"roll": "false"}
        expected = LifecycleResponse({
            "message": "some details",
            "status": "ALL_OK"
        })

        self.domino_client_mock.send_command.return_value = DominoServiceTest._prepare_response(True)

        # when
        result = self.domino_service.execute_lifecycle_command(DominoCommand.DEPLOY_VERSION, "app1", version="1.0.0")

        # then
        self._assert_client_call("/lifecycle/app1/deploy/1.0.0", expected_query_params=query)
        self.assertEqual(result.__dict__, expected.__dict__)

    def test_should_execute_lifecycle_command_of_rolling_deploy_with_success(self):

        # given
        query = {"roll": "true"}
        expected = LifecycleResponse({
            "message": "some details",
            "status": "ALL_OK"
        })

        self.domino_client_mock.send_command.return_value = DominoServiceTest._prepare_response(True)

        # when
        result = self.domino_service.execute_lifecycle_command(DominoCommand.DEPLOY_VERSION, "app1", version="1.0.0", roll=True)

        # then
        self._assert_client_call("/lifecycle/app1/deploy/1.0.0", expected_query_params=query)
        self.assertEqual(result.__dict__, expected.__dict__)

    def test_should_execute_lifecycle_command_of_instance_deploy_with_success(self):

        # given
        query = {"roll": "false", "instance": "primary"}

        expected = LifecycleResponse({
            "message": "some details",
            "status": "ALL_OK"
        })

        self.domino_client_mock.send_command.return_value = DominoServiceTest._prepare_response(True)

        # when
        result = self.domino_service.execute_lifecycle_command(DominoCommand.DEPLOY_VERSION, "app1", version="1.0.0", instance="primary")

        # then
        self._assert_client_call("/lifecycle/app1/deploy/1.0.0", expected_query_params=query)
        self.assertEqual(result.__dict__, expected.__dict__)

    def test_should_execute_lifecycle_command_with_failure(self):

        # given
        query = {"roll": "false"}

        self.domino_client_mock.send_command.return_value = DominoServiceTest._prepare_response(False)

        # when
        throwing = lambda: self.domino_service.execute_lifecycle_command(DominoCommand.START, "app2")

        # then
        self.assertRaises(DominoServiceException, throwing)
        self._assert_client_call("/lifecycle/app2/start", expected_query_params=query)

    def test_should_execute_lifecycle_command_handle_exception(self):

        # given
        query = {"roll": "false"}

        self.domino_client_mock.send_command.side_effect = Exception("Mock client call failure")

        # when
        throwing = lambda: self.domino_service.execute_lifecycle_command(DominoCommand.STOP, "app3")

        # then
        self.assertRaises(Exception, throwing)
        self._assert_client_call("/lifecycle/app3/stop", expected_method=HTTPMethod.DELETE, expected_query_params=query)

    @mock.patch("builtins.open", new_callable=mock.mock_open, read_data=_TEXT_DATA)
    def test_should_execute_import_definition_command_using_default_path_with_success(self, open_mock):

        # given
        self.domino_client_mock.send_command.return_value = DominoServiceTest._prepare_response(True, True)

        # when
        self.domino_service.import_definition()

        # then
        self._assert_client_call("/deployments/import", HTTPMethod.POST, _TEXT_DATA)

    @mock.patch("builtins.open", new_callable=mock.mock_open, read_data=_TEXT_DATA)
    def test_should_execute_import_definition_command_using_defined_path_with_success(self, open_mock):

        # given
        self.domino_client_mock.send_command.return_value = DominoServiceTest._prepare_response(True, True)

        # when
        self.domino_service.import_definition("/opt/deployment.yml")

        # then
        self._assert_client_call("/deployments/import", HTTPMethod.POST, _TEXT_DATA)

    @mock.patch("builtins.open", new_callable=mock.mock_open, read_data=_TEXT_DATA)
    def test_should_execute_import_definition_command_with_server_error(self, open_mock):

        # given
        self.domino_client_mock.send_command.return_value = DominoServiceTest._prepare_response(False)

        # when
        throwing = lambda: self.domino_service.import_definition()

        # then
        self.assertRaises(DominoServiceException, throwing)
        self._assert_client_call("/deployments/import", HTTPMethod.POST, _TEXT_DATA)

    @mock.patch("builtins.open", side_effect=IOError("Failed to open file"))
    def test_should_execute_import_definition_command_with_client_error(self, open_mock):

        # when
        throwing = lambda: self.domino_service.import_definition()

        # then
        self.assertEqual(self.domino_client_mock.send_command.call_count, 0)
        self.assertRaises(IOError, throwing)

    @mock.patch("builtins.open", new_callable=mock.mock_open, read_data=_TEXT_DATA)
    def test_should_import_oauth_descriptor_command_using_default_path_with_success(self, open_mock):

        # given
        self.domino_client_mock.send_command.return_value = DominoServiceTest._prepare_response(True, True)

        # when
        self.domino_service.import_oauth_descriptor("app", False)

        # then
        self._assert_client_call("/deployments/app/oauth-application/import", HTTPMethod.POST, _TEXT_DATA)

    @mock.patch("builtins.open", new_callable=mock.mock_open, read_data=_TEXT_DATA)
    def test_should_import_oauth_descriptor_command_using_given_path_with_success(self, open_mock):

        # given
        self.domino_client_mock.send_command.return_value = DominoServiceTest._prepare_response(True, True)

        # when
        self.domino_service.import_oauth_descriptor("app", True, "/opt/custom-oauth.yml")

        # then
        self._assert_client_call("/deployments/app/oauth-application/import", HTTPMethod.POST, _TEXT_DATA, {"dry-run": "true"})

    @mock.patch("builtins.open", new_callable=mock.mock_open, read_data=_TEXT_DATA)
    def test_should_import_oauth_descriptor_command_with_server_error(self, open_mock):

        # given
        self.domino_client_mock.send_command.return_value = DominoServiceTest._prepare_response(False)

        # when
        throwing = lambda: self.domino_service.import_oauth_descriptor("app", False)

        # then
        self.assertRaises(DominoServiceException, throwing)
        self._assert_client_call("/deployments/app/oauth-application/import", HTTPMethod.POST, _TEXT_DATA)

    @mock.patch("builtins.open", side_effect=IOError("Failed to open file"))
    def test_should_import_oauth_descriptor_command_with_client_error(self, open_mock):

        # when
        throwing = lambda: self.domino_service.import_oauth_descriptor("app", False)

        # then
        self.assertEqual(self.domino_client_mock.send_command.call_count, 0)
        self.assertRaises(IOError, throwing)

    def _assert_client_call(self, expected_path, expected_method=HTTPMethod.PUT, expected_body=None, expected_query_params=None):

        self.assertEqual(self.domino_client_mock.send_command.call_count, 1)
        domino_request: DominoRequest = self._extract_call_parameter()
        self.assertEqual(domino_request.method, expected_method)
        self.assertEqual(domino_request.path, expected_path)
        self.assertEqual(domino_request.authenticated, True)
        self.assertEqual(domino_request.body, expected_body)
        self.assertEqual(domino_request.query, expected_query_params)

    def _extract_call_parameter(self):
        return self.domino_client_mock.send_command.mock_calls[0][1][0]

    @staticmethod
    def _prepare_response(successful: bool, suppress_content: bool = False) -> Response:

        response: Response = mock.create_autospec(Response)
        if successful:
            response.status_code = 200
            if not suppress_content:
                response.content = "{}".encode("utf-8")
            response.json.return_value = {"message": "some details", "status": "ALL_OK"}
        else:
            response.status_code = 500

        return response


if __name__ == "__main__":
    unittest.main()
