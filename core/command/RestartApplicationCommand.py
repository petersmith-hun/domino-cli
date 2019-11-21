from core.command.AbstractLifecycleCommand import AbstractLifecycleCommand
from core.domain.DominoCommand import DominoCommand
from core.service.DominoService import DominoService

_COMMAND_NAME = "restart"


class RestartApplicationCommand(AbstractLifecycleCommand):
    """
    Lifecycle command implementation being able to send a restart command for the given application.
    """
    def __init__(self, domino_service: DominoService):
        super().__init__(_COMMAND_NAME, domino_service, DominoCommand.RESTART)
        self._domino_service = domino_service
