from textual.app import App

from domino_cli.core.domain.CommandDescriptor import CommandDescriptor
from domino_cli.core.service.CommandProcessor import CommandProcessor
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
    def __init__(self, app: App, command_processor: CommandProcessor):
        super().__init__(app)
        self._command_processor = command_processor

    def _action(self, event: LifecycleMessage):
        version_segment = f" {event.version}" if event.version and len(event.version) > 0 else ""
        roll_segment = "--roll" if event.roll else ""
        instance_segment = f"--instance {event.instance}" if event.instance and len(event.instance) > 0 else ""

        command = CommandDescriptor(f"{event.operation} {event.deployment_id}{version_segment} {roll_segment}{instance_segment}")

        self._command_processor.execute_command(command)
        self._app.call_from_thread(self._show_loading_indicator, False)
