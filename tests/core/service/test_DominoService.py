import unittest
from unittest import mock

from requests import Response

from domino_cli.core.client.DominoClient import DominoClient
from domino_cli.core.domain.DominoCommand import DominoCommand
from domino_cli.core.domain.DominoRequest import DominoRequest
from domino_cli.core.domain.HTTPMethod import HTTPMethod
from domino_cli.core.service.DominoService import DominoService

_TEXT_DATA = "domino:\n\tdeployments:\n\t\tleaflet\n"


class DominoServiceTest(unittest.TestCase):

    def setUp(self) -> None:
        self.domino_client_mock: DominoClient = mock.create_autospec(DominoClient)
        self.domino_service: DominoService = DominoService(self.domino_client_mock)

    @mock.patch("builtins.print", side_effect=print)
    def test_should_execute_lifecycle_command_with_success(self, print_mock):

        # given
        self.domino_client_mock.send_command.return_value = DominoServiceTest._prepare_response(True)

        # when
        self.domino_service.execute_lifecycle_command(DominoCommand.DEPLOY_VERSION, "app1", version="1.0.0")

        # then
        self._assert_client_call("/lifecycle/app1/deploy/1.0.0")
        self.assertEqual(print_mock.call_count, 6)
        print_mock.assert_has_calls([
            mock.call("[info ] Sending DEPLOY_VERSION command for application app1 via Domino"),
            mock.call("[info ] Command DEPLOY_VERSION successfully executed on application app1"),
            mock.call("[info ]  --- Response details ---"),
            mock.call("[info ]              message: some details"),
            mock.call("[info ]               status: ALL_OK"),
            mock.call()
        ])

    @mock.patch("builtins.print", side_effect=print)
    def test_should_execute_lifecycle_command_with_failure(self, print_mock):

        # given
        self.domino_client_mock.send_command.return_value = DominoServiceTest._prepare_response(False)

        # when
        self.domino_service.execute_lifecycle_command(DominoCommand.START, "app2")

        # then
        self._assert_client_call("/lifecycle/app2/start")
        print_mock.assert_has_calls([
            mock.call("[info ] Sending START command for application app2 via Domino"),
            mock.call("[error] Failed to execute command START on application app2 - Domino responded with 500")
        ])

    @mock.patch("builtins.print", side_effect=print)
    def test_should_execute_lifecycle_command_handle_exception(self, print_mock):

        # given
        self.domino_client_mock.send_command.side_effect = Exception("Mock client call failure")

        # when
        self.domino_service.execute_lifecycle_command(DominoCommand.STOP, "app3")

        # then
        self._assert_client_call("/lifecycle/app3/stop", expected_method=HTTPMethod.DELETE)
        print_mock.assert_has_calls([
            mock.call("[info ] Sending STOP command for application app3 via Domino"),
            mock.call("[error] Failed to execute HTTP request [DELETE /lifecycle/app3/stop] - reason: Mock client call failure")
        ])

    @mock.patch("builtins.open", new_callable=mock.mock_open, read_data=_TEXT_DATA)
    @mock.patch("builtins.print", side_effect=print)
    def test_should_execute_import_definition_command_using_default_path_with_success(self, print_mock, open_mock):

        # given
        self.domino_client_mock.send_command.return_value = DominoServiceTest._prepare_response(True, True)

        # when
        self.domino_service.import_definition()

        # then
        self._assert_client_call("/deployments/import", HTTPMethod.POST, _TEXT_DATA)
        self.assertEqual(print_mock.call_count, 4)
        print_mock.assert_has_calls([
            mock.call("[info ] Requesting Domino to import deployment definition from=.domino/deployment.yml"),
            mock.call("[info ] Successfully imported definition .domino/deployment.yml"),
            mock.call("[info ] No further response received from Domino"),
            mock.call()
        ])

    @mock.patch("builtins.open", new_callable=mock.mock_open, read_data=_TEXT_DATA)
    @mock.patch("builtins.print", side_effect=print)
    def test_should_execute_import_definition_command_using_defined_path_with_success(self, print_mock, open_mock):

        # given
        self.domino_client_mock.send_command.return_value = DominoServiceTest._prepare_response(True, True)

        # when
        self.domino_service.import_definition("/opt/deployment.yml")

        # then
        self._assert_client_call("/deployments/import", HTTPMethod.POST, _TEXT_DATA)
        self.assertEqual(print_mock.call_count, 4)
        print_mock.assert_has_calls([
            mock.call("[info ] Requesting Domino to import deployment definition from=/opt/deployment.yml"),
            mock.call("[info ] Successfully imported definition /opt/deployment.yml"),
            mock.call("[info ] No further response received from Domino"),
            mock.call()
        ])

    @mock.patch("builtins.open", new_callable=mock.mock_open, read_data=_TEXT_DATA)
    @mock.patch("builtins.print", side_effect=print)
    def test_should_execute_import_definition_command_with_server_error(self, print_mock, open_mock):

        # given
        self.domino_client_mock.send_command.return_value = DominoServiceTest._prepare_response(False)

        # when
        self.domino_service.import_definition()

        # then
        self._assert_client_call("/deployments/import", HTTPMethod.POST, _TEXT_DATA)
        self.assertEqual(print_mock.call_count, 4)
        print_mock.assert_has_calls([
            mock.call("[info ] Requesting Domino to import deployment definition from=.domino/deployment.yml"),
            mock.call("[error] Failed to import deployment definition .domino/deployment.yml - Domino responded with 500"),
            mock.call("[info ] No further response received from Domino"),
            mock.call()
        ])

    @mock.patch("builtins.open", side_effect=IOError("Failed to open file"))
    @mock.patch("builtins.print", side_effect=print)
    def test_should_execute_import_definition_command_with_client_error(self, print_mock, open_mock):

        # when
        self.domino_service.import_definition()

        # then
        self.assertEqual(self.domino_client_mock.send_command.call_count, 0)
        self.assertEqual(print_mock.call_count, 2)
        print_mock.assert_has_calls([
            mock.call("[info ] Requesting Domino to import deployment definition from=.domino/deployment.yml"),
            mock.call("[error] Failed to import definition from .domino/deployment.yml - reason: Failed to open file")
        ])

    def _assert_client_call(self, expected_path, expected_method=HTTPMethod.PUT, expected_body=None):

        self.assertEqual(self.domino_client_mock.send_command.call_count, 1)
        domino_request: DominoRequest = self._extract_call_parameter()
        self.assertEqual(domino_request.method, expected_method)
        self.assertEqual(domino_request.path, expected_path)
        self.assertEqual(domino_request.authenticated, True)
        self.assertEqual(domino_request.body, expected_body)

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
