from textual.app import App
from textual.widgets import LoadingIndicator


class ActionAdapter[E]:

    def __init__(self, app: App):
        self._app = app

    def execute(self, event: E = None):
        pass


class LongRunningActionAdapter[E](ActionAdapter[E]):

    def __init__(self, app: App):
        super().__init__(app)

    def execute(self, event: E = None):
        self._show_loading_indicator(True)
        self._app.run_worker(lambda: self._worker(event), thread=True)

    def _worker(self, event: E):
        try:
            self._action(event)
        finally:
            self._show_loading_indicator(False)

    def _action(self, event: E):
        pass

    def _show_loading_indicator(self, show: bool):
        self._app.query_one(LoadingIndicator).display = show
