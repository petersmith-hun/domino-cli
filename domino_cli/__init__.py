"""
domino_cli.py :: Main entry point for Domino CLI application.
"""

__version__ = "3.0.0"

from domino_cli.core.ApplicationContext import ApplicationContext


def main() -> None:
    # TODO make this configurable
    # ApplicationContext.init_cli(__version__).run_loop()
    ApplicationContext.init_tui(__version__).run()
