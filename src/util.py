"""
General utils for things - mostly file path resolution
"""

import os

path_root = os.path.realpath(__file__).replace("util.py", "")


def rel_to_abspath(path: str) -> str:
    """
    Converts a local path (like '../thing' to the absolute path)
    """
    return f"{path_root}{path}".replace("\\", os.sep).replace("/", os.sep)
