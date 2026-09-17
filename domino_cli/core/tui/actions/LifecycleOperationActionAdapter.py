from textual.app import App

from domino_cli.core.domain.CustomExceptions import DominoServiceException
from domino_cli.core.domain.Deployments import LifecycleResponse
from domino_cli.core.domain.DominoCommand import DominoCommand
from domino_cli.core.service.DominoService import DominoService
from domino_cli.core.tui.actions import LongRunningActionAdapter


class LifecycleMessage:
    """
    TODO.
    """
    def __init__(self, operation: str, deployment_id: str, roll: bool, instance: str, version: str | None):
        self.operation = operation
        self.deployment_id = deployment_id
        self.roll = roll
        self.instance = instance
        self.version = version


class LifecycleOperationActionAdapter(LongRunningActionAdapter[LifecycleMessage]):
    """
    TODO.
    """
    _command_map = {
        "deploy_latest": DominoCommand.DEPLOY_LATEST,
        "deploy_version": DominoCommand.DEPLOY_VERSION,
        "start": DominoCommand.START,
        "stop": DominoCommand.STOP,
        "restart": DominoCommand.RESTART,
        "info": DominoCommand.INFO
    }

    def __init__(self, app: App, domino_service: DominoService):
        super().__init__(app)
        self._domino_service = domino_service

    def _action(self, event: LifecycleMessage):

        instance_suffix = f".{event.instance}" if event.instance else ""

        try:
            result = self._domino_service.execute_lifecycle_command(
                self._command_map[event.operation], event.deployment_id, event.version, event.roll, event.instance)
            details = self._create_success_details(event, result, instance_suffix)

            self._app.notify(details, title="Lifecycle operation completed", severity="information", markup=True, timeout=10)

        except DominoServiceException as exc:

            content = self._create_error_reason(event, exc, instance_suffix)
            self._app.notify(content, title="Lifecycle operation failed", severity="error")

    @staticmethod
    def _create_success_details(event: LifecycleMessage, result: LifecycleResponse | dict, instance_suffix) -> str:

        details = f"Operation {event.operation} has been successfully executed on application [i]{event.deployment_id}{instance_suffix}[/i]\n\n"
        details = details + "Domino additionally responded with:\n"

        for field in (result.keys() if isinstance(result, dict) else result.__dict__) :
            value = result[field] if isinstance(result, dict) else result.__dict__[field]
            if value:
                details = details + f"[b]{field:>20}[/b]: {value}\n"

        return details

    @staticmethod
    def _create_error_reason(event: LifecycleMessage, exc: DominoServiceException, instance_suffix: str) -> str:

        if event.operation == "info":

            if exc.status_code == 404:
                reason = "not configured"
            elif exc.status_code == 417:
                reason = "misconfigured"
            else:
                reason = "unreachable"

            content = f"Info endpoint of application [i]{event.deployment_id}{instance_suffix}[/i] is {reason}"

        else:
            content = str(exc)

        return content
