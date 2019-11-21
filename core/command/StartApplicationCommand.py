from core.command.AbstractLifecycleCommand import AbstractLifecycleCommand
from core.domain.DominoCommand import DominoCommand
from core.service.DominoService import DominoService

_COMMAND_NAME = "start"


class StartApplicationCommand(AbstractLifecycleCommand):
    """
    Lifecycle command implementation being able to send a start command for the given application.
    """
    def __init__(self, domino_service: DominoService):
        super().__init__(_COMMAND_NAME, domino_service, DominoCommand.START)
        self._domino_service = domino_service
