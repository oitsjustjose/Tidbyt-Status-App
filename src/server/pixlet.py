"""A Python Wrapper for Pixlet ops"""

import subprocess
from os import getenv
from pathlib import Path
from platform import machine

from renderables import Renderable


class PixletHelper:
    def __init__(self):
        self.root_path: Path = Path("./").resolve()
        self.pixlet: Path = self.root_path.joinpath(f"pixlet.{machine()}").resolve()
        self.device_id: str = getenv("TIDBYT_DEVICE_ID", "")

    def push_to_tidbyt(self, renderable: Renderable) -> None:
        """Pushes a renderable to the Tidbyt device

        Args:
            renderable (Renderable): The Pixlet Configuration for the given state
        """
        self.__display(self.__render(renderable))

    def __render(self, renderable: Renderable) -> Path:
        """Renders a given PixeltConfiguration (and any template args) to webp

        Args:
            renderable (Renderable): The Pixlet Configuration for the given state

        Returns:
            Path: The path to the rendered output file
        """
        output_path = self.__prepare_file(renderable)

        with subprocess.Popen([self.pixlet, "render", str(output_path)]) as proc:
            proc.wait()

        return self.root_path.joinpath("tmp.webp").resolve()

    def __display(self, path: Path) -> None:
        """Pushes a given rendered webp file to the pixlet on the same installation id

        Args:
            path (Path): The path to the given rendered webp
        """
        with subprocess.Popen(
            [
                self.pixlet,
                "push",
                "--installation-id",
                "automation",
                self.device_id,
                str(path),
            ]
        ) as proc:
            proc.wait()

    def __prepare_file(self, renderable: Renderable) -> Path:
        """Prepares a given pixlet star file. If the file is a template, checks the template keys and prepares the template before writing to the temp path

        Args:
            renderable (Renderable): The Pixlet Configuration for the given state

        Raises:
            Exception: Thrown if a required key defined in the Renderable is missing

        Returns:
            Path: The path to the output file
        """
        output_path = self.root_path.joinpath("tmp.star").resolve()

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
