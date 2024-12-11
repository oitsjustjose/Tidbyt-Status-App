"""
General utils for things - mostly file path resolution
"""

import os


class Renderable:
    """A simple renderable baseclass"""

    def render(self) -> None:
        """Renders to Pixlet"""
        raise Exception("Default class implementation is not supported!")


def rel_to_abspath(path: str) -> str:
    """
    Converts a local path (like '../thing' to the absolute path)
    """
    path_root = os.path.realpath(__file__).replace("util.py", "")
    return f"{path_root}{path}".replace("\\", os.sep).replace("/", os.sep)
