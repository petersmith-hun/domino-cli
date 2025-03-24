import unittest
from unittest import mock

from domino_cli.core.domain.SessionContext import SessionContext
from domino_cli.core.service.SessionContextHolder import SessionContextHolder


class SessionContextHolderTest(unittest.TestCase):

    def setUp(self) -> None:
        self.session_context_holder: SessionContextHolder = SessionContextHolder()

    @mock.patch("builtins.print", side_effect=print)
    def test_should_get_bearer_auth_return_none_without_updating_context(self, print_mock):

        # when
        result: dict = self.session_context_holder.get_bearer_auth()

        # then
        self.assertIsNone(result)
        print_mock.assert_called_once_with("[warn ] Session is not yet open!")

    def test_should_get_bearer_auth_return_authorization_header_after_updating_context(self):

        # given
        session_context: SessionContext = SessionContext("user", "jwt_token")
        self.session_context_holder.update(session_context)

        # when
        result: dict = self.session_context_holder.get_bearer_auth()

        # then
        self.assertEqual(result, {"Authorization": "Bearer jwt_token"})


if __name__ == "__main__":
    unittest.main()
