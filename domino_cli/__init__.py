"""
domino_cli.py :: Main entry point for Domino CLI application.
"""

__version__ = "2.1.0"

import os

from domino_cli.core.ApplicationContext import ApplicationContext


def _set_work_dir() -> None:
    script_path: str = os.path.realpath(__file__)
    script_dir: str = os.path.dirname(script_path)
    os.chdir(script_dir)


def main() -> None:
    _set_work_dir()
    ApplicationContext.init_cli(__version__).run_loop()
