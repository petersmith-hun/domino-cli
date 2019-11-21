
"""
domino_cli.py :: Main entry point for Domino CLI application.
"""

__version__ = "1.0.0"

from core.ApplicationContext import ApplicationContext


if __name__ == "__main__":
    ApplicationContext.init_cli().run_loop()
