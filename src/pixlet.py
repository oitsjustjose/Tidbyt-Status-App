"""
Python wrapper for Pixlet Operations
"""

import subprocess
import os
from util import rel_to_abspath

STARTUP_INFO = subprocess.STARTUPINFO()
STARTUP_INFO.dwFlags |= subprocess.STARTF_USESHOWWINDOW


def update_template(template_path: str, out_path: str, replacers: dict):
    """
    Opens the template up at template_path, reads it in,
     replaces all keys in replacers with their values
     then writes it out with the same name in `./out`
    Arguments:
        template_path (str): the path of the template.star to load
        out_path (str): where the output should be saved
        replacers (dict): a Dict[str,str] whose keys are in the template,
            and whose values will replace their keys in the template
    """
    if not os.path.exists(rel_to_abspath("../out")):
        os.mkdir(rel_to_abspath("../out"))
    with open(template_path, "r", encoding="utf-8") as file_handle:
        data = file_handle.read()
    for key in replacers:
        data = data.replace(key, replacers[key])
    with open(out_path, "w", encoding="utf-8") as file_handle:
        file_handle.write(data)


def display(file_path: str, installation_id: str = None):
    """
    Displays a file (by name) to the Tidbyt, reading the device id from `device_id`
    """
    with open(rel_to_abspath("../device_id"), "r", encoding="utf-8") as file_handle:
        device_id = file_handle.read()
    if installation_id:
        args = [
            rel_to_abspath("../pixlet.exe"),
            "push",
            "--installation-id",
            installation_id,
            device_id,
            file_path,
        ]
    else:
        args = [
            rel_to_abspath("../pixlet.exe"),
            "push",
            device_id,
            file_path,
        ]

    with subprocess.Popen(args, startupinfo=STARTUP_INFO) as process:
        process.wait()


def render(file_path: str):
    """
    Uses Pixlet to render a `.star` file to webp so that it can be pushed
    Args:
        file_path (str): the path (relative) to the file you want rendered
    """
    with subprocess.Popen(
        [rel_to_abspath("../pixlet.exe"), "render", file_path],
        startupinfo=STARTUP_INFO,
    ) as process:
        process.wait()
