
"""
domino_cli.py :: Main entry point for Domino CLI application.
"""

__version__ = "1.3.0"

import os

from core.ApplicationContext import ApplicationContext


def _set_work_dir() -> None:
    script_path: str = os.path.realpath(__file__)
    script_dir: str = os.path.dirname(script_path)
    os.chdir(script_dir)


if __name__ == "__main__":
    _set_work_dir()
    ApplicationContext.init_cli(__version__).run_loop()
