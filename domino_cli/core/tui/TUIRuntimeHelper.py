import datetime

from textual.app import App
from textual.notifications import SeverityLevel
from textual.widgets import Label
from typing_extensions import Any

from domino_cli.core.cli import LogLevel
from domino_cli.core.domain.SessionContext import SessionContext


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
    def set_authenticated(cls, session_context: SessionContext):

        if cls._is_authenticated_label is None:
            return

        expiration_delta = session_context.expires_at - datetime.datetime.now()

        if expiration_delta.days > 0:
            expires_in = f"{expiration_delta.days} day(s)"
        elif expiration_delta.seconds > 3600:
            expires_in = f"{expiration_delta.seconds // 3600} hour(s)"
        else:
            expires_in = f"{expiration_delta.seconds // 60} minute(s)"

        cls._is_authenticated_label.update(f"✔ (Expires in {expires_in})")
        cls._is_authenticated_label.styles.color = "green"

    @classmethod
    def log_to_toast(cls, log_level: LogLevel, message):
        severity: SeverityLevel = cls._severity_map.get(log_level, "information")
        cls._observer.notify(severity, message)
