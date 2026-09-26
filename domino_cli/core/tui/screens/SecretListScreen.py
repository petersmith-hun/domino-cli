from typing import cast

from textual.containers import HorizontalGroup
from textual.widgets import ListView, Label, ListItem

from domino_cli.core.domain.Secrets import SecretDetails, SecretGroup
from domino_cli.core.service.SecretService import SecretService
from domino_cli.core.tui.modals.ContextOptionsModal import ContextOptionsModal
from domino_cli.core.tui.modals.SecretOptionsModal import SecretOptionsModal


class SecretLabel(Label):

    DEFAULT_CSS = """
    SecretLabel {
        padding: 0 2;
    }
    """
    def __init__(self, text: str, long_field: bool = False):
        super().__init__(text if text else "")
        if long_field:
            self.styles.width = "2fr"
        else:
            self.styles.width = "1fr"


class SecretListItem(ListItem):

    DEFAULT_CSS = """
    SecretListItem {
        padding: 1 2;
        outline-top: none;
        outline-bottom: none;
        outline-left: ascii $accent;
        outline-right: ascii $accent;
    }
    """

    def __init__(self, secret: SecretDetails):

        labels = [
            SecretLabel(secret.key, long_field=True),
            SecretLabel(secret.last_accessed_by),
            SecretLabel(secret.last_accessed_at),
            SecretLabel(secret.created_at),
            SecretLabel(secret.updated_at)
        ]

        if secret.retrievable == "Retrievable":
            labels.append(SecretLabel("Retrievable"))
        else:
            labels.append(SecretLabel("Yes" if secret.retrievable else "No"))

        super().__init__(HorizontalGroup(*labels))
        self.secret_details = secret


class ContextListItem(ListItem):

    DEFAULT_CSS = """
    ContextListItem {
        padding: 1 2;
        outline-top: none;
        outline-bottom: none;
        outline-left: ascii $accent;
        outline-right: ascii $accent;
        background: $background;
    }
    
    HorizontalGroup {
        width: 100%;
        text-align: center;
    }
    
    SecretLabel {
        width: 100%;
        text-align: center;
    }
    """
    def __init__(self, secret_group: SecretGroup):
        super().__init__(HorizontalGroup(
            SecretLabel(secret_group.context)
        ))
        self.key = secret_group.context


class SecretListHeader(SecretListItem):

    DEFAULT_CSS = """
    SecretListHeader {
        text-style: bold;
        background: $boost;
    }
    """
    _HEADER = SecretDetails({
        "key": "Key",
        "lastAccessedBy": "Last accessed by",
        "lastAccessedAt": "Last accessed at",
        "createdAt": "Created at",
        "updatedAt": "Last updated at",
        "retrievable": "Retrievable"
    })

    def __init__(self):
        super().__init__(self._HEADER)


class SecretListScreen(ListView):

    DEFAULT_CSS = """
    SecretListScreen {
        background: $surface;
        outline-left: ascii $accent;
        outline-right: ascii $accent;
        outline-bottom: ascii $accent;
    }
    """
    def __init__(self, secret_service: SecretService):
        super().__init__(id="secrets")
        self._secret_service = secret_service

    def action_select_cursor(self) -> None:

        if isinstance(self.highlighted_child, SecretListHeader):
            return

        elif isinstance(self.highlighted_child, SecretListItem):
            secret = cast(SecretListItem, self.highlighted_child)
            self.app.push_screen(SecretOptionsModal(self._secret_service, secret.secret_details))

        elif isinstance(self.highlighted_child, ContextListItem):
            secret_context = cast(ContextListItem, self.highlighted_child)
            self.app.push_screen(ContextOptionsModal(self._secret_service, secret_context.key))
