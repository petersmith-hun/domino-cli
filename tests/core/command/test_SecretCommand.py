import unittest
from unittest import mock
from unittest.mock import call

from domino_cli.core.command.SecretCommand import SecretCommand
from domino_cli.core.command.dsl.dsm.DSLCreate import CreateSecretCommandProcessor
from domino_cli.core.command.dsl.dsm.DSLDelete import DeleteSecretCommandProcessor
from domino_cli.core.command.dsl.dsm.DSLLocking import LockSecretCommandProcessor, UnlockSecretCommandProcessor
from domino_cli.core.command.dsl.dsm.DSLMain import MainSecretCommandProcessor
from domino_cli.core.command.dsl.dsm.DSLMetadata import MetadataCommandProcessor, MetadataAllCommandProcessor, \
    MetadataKeyCommandProcessor
from domino_cli.core.command.dsl.dsm.DSLRetrieval import RetrievalSecretCommandProcessor, \
    RetrieveByKeySecretCommandProcessor, RetrieveByContextSecretCommandProcessor
from domino_cli.core.domain.CommandDescriptor import CommandDescriptor
from domino_cli.core.service.SecretService import SecretService
from tests.core.command.CommandBaseTest import CommandBaseTest


class SecretCommandTest(CommandBaseTest):

    def setUp(self) -> None:
        self.secret_service_mock = mock.create_autospec(SecretService)

        self.secret_command: SecretCommand = SecretCommand([
            MainSecretCommandProcessor(),
            CreateSecretCommandProcessor(self.secret_service_mock),
            MetadataCommandProcessor(),
            MetadataAllCommandProcessor(self.secret_service_mock),
            MetadataKeyCommandProcessor(self.secret_service_mock),
            RetrievalSecretCommandProcessor(),
            RetrieveByKeySecretCommandProcessor(self.secret_service_mock),
            RetrieveByContextSecretCommandProcessor(self.secret_service_mock),
            LockSecretCommandProcessor(self.secret_service_mock),
            UnlockSecretCommandProcessor(self.secret_service_mock),
            DeleteSecretCommandProcessor(self.secret_service_mock),
        ])

    @mock.patch("domino_cli.core.command.dsl.dsm.DSLCreate.getpass", return_value="new-secret-value")
    def test_execute_command_process_request(self, getpass_mock):

        # given
        for (command, execute_assertion) in self._prepare_secret_calls():
            with self.subTest("test processing secret command", command=command):

                command_descriptor: CommandDescriptor = CommandDescriptor(command)

                # when
                self.secret_command.execute_command(command_descriptor)

                # then
                execute_assertion()
                self.secret_service_mock.reset_mock()

    @mock.patch("builtins.print", side_effect=print)
    def test_should_execute_command_fail_on_validation(self, print_mock):

        # given
        for (command, expected_validation_error) in self._prepare_failing_calls():
            with self.subTest("test processing secret command", command=command):

                print_mock.reset_mock()
                command_descriptor: CommandDescriptor = CommandDescriptor(command)

                # when
                self.secret_command.execute_command(command_descriptor)

                # then
                self.assertEqual(self.secret_service_mock.call_count, 0)
                self.assertEqual(print_mock.call_count, 2)
                print_mock.assert_has_calls([
                    call(expected_validation_error),
                    call("[error] Domino CLI was not able to process your secret management request")
                ])

    def test_should_command_be_applicable_for_secret_command(self):

        self.applicability_check(self.secret_command, "secret")

    def _prepare_secret_calls(self):

        return [
            ("secret --create new.secret ctx", lambda: self.secret_service_mock.create_secret.assert_called_once_with("new.secret", "ctx", "new-secret-value")),
            ("secret --metadata --all", lambda: self.secret_service_mock.get_all_metadata.assert_called_once()),
            ("secret --metadata config.test", lambda: self.secret_service_mock.get_metadata_by_key.assert_called_once_with("config.test")),
            ("secret --retrieve --key config.test", lambda: self.secret_service_mock.retrieve_secret_by_key.assert_called_once_with("config.test")),
            ("secret --retrieve --context ctx", lambda: self.secret_service_mock.retrieve_secrets_by_context.assert_called_once_with("ctx")),
            ("secret --lock secret.unlocked", lambda: self.secret_service_mock.lock_secret.assert_called_once_with("secret.unlocked")),
            ("secret --unlock secret.locked", lambda: self.secret_service_mock.unlock_secret.assert_called_once_with("secret.locked")),
            ("secret --delete to.be.deleted", lambda: self.secret_service_mock.delete_secret.assert_called_once_with("to.be.deleted"))
        ]

    @staticmethod
    def _prepare_failing_calls():

        return [
            ("secret", "[error] Too few arguments, first argument must be either: --create | --metadata | --retrieve | --lock | --unlock | --delete"),
            ("secret --invalid-command", "[error] Invalid subcommand, first argument must be either: --create | --metadata | --retrieve | --lock | --unlock | --delete"),

            ("secret --create", "[error] Invalid arguments, expected usage: secret --create <key> <context> (then you'll be prompted to enter the secret value)"),
            ("secret --create config.test", "[error] Invalid arguments, expected usage: secret --create <key> <context> (then you'll be prompted to enter the secret value)"),
            ("secret --create config.test ctx invalid-extra", "[error] Invalid arguments, expected usage: secret --create <key> <context> (then you'll be prompted to enter the secret value)"),

            ("secret --metadata", "[error] Too few arguments, first argument must be either: --all | <key>"),
            ("secret --metadata config.test invalid-extra", "[error] Invalid arguments, expected usage: secret --metadata <key>"),

            ("secret --retrieve", "[error] Too few arguments, must be either: --key <key> | --context <context>"),
            ("secret --retrieve invalid-arg-1 invalid-arg-2 invalid-arg-3", "[error] Too many arguments, must be either: --key <key> | --context <context>"),
            ("secret --retrieve invalid-subcommand config.test", "[error] Invalid subcommand, first argument must be either: --key | --context"),
            ("secret --retrieve --key", "[error] Invalid arguments, expected usage: secret --retrieve --key <key>"),
            ("secret --retrieve --context", "[error] Invalid arguments, expected usage: secret --retrieve --context <context>"),

            ("secret --lock", "[error] Invalid arguments, expected usage: secret --lock <key>"),
            ("secret --lock config.test invalid-extra", "[error] Invalid arguments, expected usage: secret --lock <key>"),

            ("secret --unlock", "[error] Invalid arguments, expected usage: secret --unlock <key>"),
            ("secret --unlock config.test invalid-extra", "[error] Invalid arguments, expected usage: secret --unlock <key>"),

            ("secret --delete", "[error] Invalid arguments, expected usage: secret --delete <key>"),
            ("secret --delete config.test invalid-extra", "[error] Invalid arguments, expected usage: secret --delete <key>"),
        ]

if __name__ == "__main__":
    unittest.main()
