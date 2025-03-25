"""
domino_cli.py :: Main entry point for Domino CLI application.
"""

__version__ = "2.3.0"

from domino_cli.core.ApplicationContext import ApplicationContext


def main() -> None:
    ApplicationContext.init_cli(__version__).run_loop()
