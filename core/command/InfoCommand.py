from core.command.AbstractLifecycleCommand import AbstractLifecycleCommand
from core.domain.DominoCommand import DominoCommand
from core.service.DominoService import DominoService

_COMMAND_NAME = "info"


class InfoCommand(AbstractLifecycleCommand):
    """
    Lifecycle command implementation being able to send an info request command for the given application.
    """
    def __init__(self, domino_service: DominoService):
        super().__init__(_COMMAND_NAME, domino_service, DominoCommand.INFO)
        self._domino_service = domino_service
