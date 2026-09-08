from textual.app import App
from textual.notifications import SeverityLevel
from textual.widgets import Label
from typing_extensions import Any

from domino_cli.core.cli import LogLevel


class Observer:
    def __init__(self):
        self._observers = []

    def register(self, observer):
        self._observers.append(observer)

    def notify(self, severity: SeverityLevel, message: str):
        for observer in self._observers:
            observer(severity, message)


class TUIRuntimeHelper:

    _observer = Observer()
    _severity_map: dict[LogLevel, SeverityLevel] = {
        LogLevel.INFO: "information",
        LogLevel.WARNING: "warning",
        LogLevel.ERROR: "error"
    }
    _is_authenticated_label: Label | None = None

    @classmethod
    def register_toast(cls, tui_app: App[Any]):
        cls._observer.register(lambda severity, message: tui_app.notify(message, title="Command result", severity=severity, timeout=10, markup=False))

    @classmethod
    def register_is_authenticated_hook(cls, is_authenticated_label: Label):
        cls._is_authenticated_label = is_authenticated_label

    @classmethod
    def set_authenticated(cls):

        if cls._is_authenticated_label is None:
            return

        cls._is_authenticated_label.update("✔")
        cls._is_authenticated_label.styles.color = "green"

    @classmethod
    def log_to_toast(cls, log_level: LogLevel, message):
        severity: SeverityLevel = cls._severity_map.get(log_level, "information")
        cls._observer.notify(severity, message)
