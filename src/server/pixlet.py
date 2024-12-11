"""A Python Wrapper for Pixlet ops"""

import subprocess
from pathlib import Path

from renderables import Renderable


ROOT_PATH = Path("./").resolve()
PIXLET_EXEC = ROOT_PATH.joinpath("pixlet").resolve()


def push_to_tidbyt(renderable: Renderable) -> None:
    """Pushes a renderable to the Tidbyt device

    Args:
        renderable (Renderable): The Pixlet Configuration for the given state
    """
    __display(__render(renderable))


def __render(renderable: Renderable) -> Path:
    """Renders a given PixeltConfiguration (and any template args) to webp

    Args:
        renderable (Renderable): The Pixlet Configuration for the given state

    Returns:
        Path: The path to the rendered output file
    """
    output_path = __prepare_file(renderable)

    with subprocess.Popen([PIXLET_EXEC, "render", str(output_path)]) as proc:
        proc.wait()

    return ROOT_PATH.joinpath("tmp.webp").resolve()


def __display(path: Path) -> None:
    """Pushes a given rendered webp file to the pixlet on the same installation id

    Args:
        path (Path): The path to the given rendered webp
    """

    with open(
        ROOT_PATH.joinpath("device_id").resolve(), "r", encoding="utf8"
    ) as handle:
        dev_id = handle.read()

    with subprocess.Popen(
        [
            PIXLET_EXEC,
            "push",
            "--installation-id",
            "automation",
            dev_id,
            str(path),
        ]
    ) as proc:
        proc.wait()


def __prepare_file(renderable: Renderable) -> Path:
    """Prepares a given pixlet star file. If the file is a template, checks the template keys and prepares the template before writing to the temp path

    Args:
        renderable (Renderable): The Pixlet Configuration for the given state

    Raises:
        Exception: Thrown if a required key defined in the Renderable is missing

    Returns:
        Path: The path to the output file
    """
    output_path = ROOT_PATH.joinpath("tmp.star").resolve()

    with open(renderable.file_path, "r", encoding="utf8") as handle:
        data = handle.read()

    if renderable.is_dynamic:
        args = renderable.resolve_template_keys()
        for key in renderable.template_keys:
            if not key in args:
                raise Exception(
                    f"Failed to render Pixlet Configuration for {renderable.for_state.name} -- missing key '{key}'"
                )
            data = data.replace(key, args[key])

    with open(output_path, "w", encoding="utf8") as handle:
        handle.write(data)

    return output_path
