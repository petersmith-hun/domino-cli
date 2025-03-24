import os
import string
import sys
from enum import Enum

from domino_cli.core.cli.RuntimeHelper import RuntimeHelper


class TerminalColor(Enum):
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    NORMAL = "\033[0m"


class LogLevel(Enum):
    INFO = "info"
    WARNING = "warn"
    ERROR = "error"

_terminal_color_mapping: dict[LogLevel, TerminalColor] = {
    LogLevel.INFO: TerminalColor.GREEN,
    LogLevel.WARNING: TerminalColor.YELLOW,
    LogLevel.ERROR: TerminalColor.RED,
}


def info(message: string) -> None:
    """
    Logs the given message on info level. Ignores logging in CI/CD mode.

    :param message: message to log
    """
    _log(LogLevel.INFO, message, False)

def warning(message: string) -> None:
    """
    Logs the given message on warn level. Ignores logging in CI/CD mode.

    :param message: message to log
    """
    _log(LogLevel.WARNING, message, False)

def error(message: string) -> None:
    """
    Logs the given message on error level. Logs the given message even in CI/CD mode.

    :param message: message to log
    """
    _log(LogLevel.ERROR, message, True)

def get_color(color: TerminalColor) -> str:
    """
    Returns the terminal color code assigned to the given TerminalColor, if using terminal colors is enabled. Otherwise,
    returns an empty string.

    :param color: TerminalColor enum constant
    :return: color code or empty string
    """
    return "" \
        if os.getenv("DOMINO_CLI_DISABLE_COLORS") is not None or "unittest" in sys.modules \
        else color.value

def _log(log_level: LogLevel, message: string, force: bool = False) -> None:

    if not RuntimeHelper.is_cicd_mode() or force:
        print(f"[{get_color(_terminal_color_mapping[log_level])}{log_level.value:5}{get_color(TerminalColor.NORMAL)}] {message}")
