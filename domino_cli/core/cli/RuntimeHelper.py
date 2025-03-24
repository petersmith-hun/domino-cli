import sys


class RuntimeHelper:
    """
    Runtime helper utilities.
    """

    _cicd_mode = len(sys.argv) > 1 and sys.argv[1] == "--cicd"

    @classmethod
    def is_cicd_mode(cls) -> bool:
        """
        Checks if the CLI was executed in CI/CD mode. CI/CD mode only allows executing a single command, defined
        directly in the command line. The same commands and parameterization should be used as before, but in order to
        run the CLI in CI/CD mode, the first parameter should be "--cicd". E.g. domino-cli --cicd deploy app 1.0.0.
        For further information, see the relevant section of the documentation in README.md.

        :return: true if CI/CD mode is enabled, false otherwise.
        """
        return cls._cicd_mode

    @classmethod
    def get_cicd_command_line(cls) -> str:
        """
        Returns the CI/CD command line, without the --cicd flag itself, only if the CLI is running in CI/CD mode.
        Otherwise, it returns None.

        :return: CI/CD command line without --cicd flag
        """
        return " ".join(sys.argv[2:]) \
            if cls._cicd_mode \
            else None

    @classmethod
    def input_wrapper(cls, input_call: lambda: str) -> str:
        """
        Checks if the CLI is running in CI/CD mode before executing an input call. If so, immediately quits, otherwise
        executes the input call.

        :param input_call: input call to be executed
        :return: result of the input call
        """
        cls.unsupported_in_cicd_mode()

        return input_call()

    @classmethod
    def exit_with_error_in_cicd_mode(cls) -> None:
        """
        Closes the CLI application with exit status 1 in CI/CD mode. Can be used to terminate the CLI on exception.
        """
        if cls._cicd_mode:
            exit(1)

    @classmethod
    def unsupported_in_cicd_mode(cls) -> None:
        """
        Closes the CLI application with exit status 1 in CI/CD mode. Can be used to terminate the CLI when an
        unsupported operation is executed in CI/CD mode.
        """
        if cls._cicd_mode:
            print("[error] This operation is not supported in CI/CD mode")
            exit(1)
