"""
domino_cli.py :: Main entry point for Domino CLI application.
"""

__version__ = "3.0.0"

from domino_cli.core.ApplicationContext import ApplicationContext
from domino_cli.core.cli.RuntimeHelper import RuntimeHelper


def main() -> None:
    if RuntimeHelper.is_cli_mode() or RuntimeHelper.is_cicd_mode():
        ApplicationContext.init_cli(__version__).run_loop()
    else:
        ApplicationContext.init_tui(__version__).run()
