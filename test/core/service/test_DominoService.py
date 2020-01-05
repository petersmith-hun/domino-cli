import unittest
from unittest import mock
from requests import Response

from core.client.DominoClient import DominoClient
from core.domain.DominoCommand import DominoCommand
from core.domain.DominoRequest import DominoRequest
from core.domain.HTTPMethod import HTTPMethod
from core.service.DominoService import DominoService


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
            mock.call("Sending DEPLOY_VERSION command for application app1 via Domino"),
            mock.call("Command DEPLOY_VERSION successfully executed on application app1"),
            mock.call(" --- Response details ---"),
            mock.call("   message: some details"),
            mock.call("    status: ALL_OK"),
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
            mock.call("Sending START command for application app2 via Domino"),
            mock.call("Failed to execute command START on application app2 - Domino responded with 500")
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
            mock.call("Sending STOP command for application app3 via Domino"),
            mock.call("Failed to execute HTTP request [DELETE /lifecycle/app3/stop] - reason Mock client call failure")
        ])

    def _assert_client_call(self, expected_path, expected_method=HTTPMethod.PUT):

        self.assertEqual(self.domino_client_mock.send_command.call_count, 1)
        domino_request: DominoRequest = self._extract_call_parameter()
        self.assertEqual(domino_request.method, expected_method)
        self.assertEqual(domino_request.path, expected_path)
        self.assertEqual(domino_request.authenticated, True)
        self.assertEqual(domino_request.body, None)

    def _extract_call_parameter(self):
        return self.domino_client_mock.send_command.mock_calls[0][1][0]

    @staticmethod
    def _prepare_response(successful: bool) -> Response:

        response: Response = mock.create_autospec(Response)
        if successful:
            response.status_code = 200
            response.json.return_value = {"message": "some details", "status": "ALL_OK"}
        else:
            response.status_code = 500

        return response


if __name__ == "__main__":
    unittest.main()
