"""A Python Wrapper for Pixlet ops"""

import logging
from os import getenv
from pathlib import Path
from platform import machine
from subprocess import PIPE, Popen
from time import sleep
from typing import Tuple

from server.renderables import Renderable


class PixletHelper:
    def __init__(self):
        self.logger = logging.getLogger("uvicorn.error")
        self.root_path: Path = Path("./").resolve()
        self.pixlet: Path = self.root_path.joinpath(f"pixlet.{machine()}").resolve()
        self.device_id: str = getenv("TIDBYT_DEVICE_ID", "")
        self.api_token: str = getenv("TIDBYT_API_TOKEN", "")

    def push_to_tidbyt(self, renderable: Renderable) -> bool:
        """Pushes a renderable to the Tidbyt device

        Args:
            renderable (Renderable): The Pixlet Configuration for the given state

        Returns:
            bool: True if the process succeeded, False otherwise
        """
        return self.__display(self.__render(renderable))

    def __render(self, renderable: Renderable) -> Path:
        """Renders a given PixeltConfiguration (and any template args) to webp

        Args:
            renderable (Renderable): The Pixlet Configuration for the given state

        Returns:
            Path: The path to the rendered output file
        """
        output_path = self.__prepare_file(renderable)

        with Popen([self.pixlet, "render", str(output_path)], stdout=PIPE, stderr=PIPE) as proc:
            exit_code = proc.wait()
            stdout, stderr = self.__get_decoded_out(proc)
            if exit_code != 0 and (stdout or stderr):
                self.logger.warning(f"__render call failed: {stdout or stderr}")

        return self.root_path.joinpath("tmp.webp").resolve()

    def __display(self, path: Path, attempt=0) -> bool:
        """Pushes a given rendered webp file to the pixlet on the same installation id

        Args:
            path (Path): The path to the given rendered webp
            attempt (int, optional): Used to track recursive calls in case pushing fails. Defaults to 0.

        Returns:
            bool: True if pushing the rendered path to the Tidbyt succeeded, False otherwise
        """
        with Popen(
            [
                self.pixlet,
                "push",
                "--api-token",
                self.api_token,
                "--installation-id",
                "automation",
                self.device_id,
                str(path),
            ],
            stdout=PIPE,
            stderr=PIPE,
        ) as proc:
            exit_code = proc.wait()
            if exit_code == 0:
                return True
            if attempt < 5:
                sleep(3 * (attempt + 1))
                return self.__display(path, attempt=attempt + 1)
            else:
                stdout, stderr = self.__get_decoded_out(proc)
                if exit_code != 0 and (stdout or stderr):
                    self.logger.warning(f"__display call failed after 5 attempts: {stdout or stderr}")
                return False

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
                if key not in args:
                    raise Exception(f"Failed to render Pixlet Configuration for {str(renderable.file_path)} -- missing key '{key}'")
                data = data.replace(key, str(args[key]))

        with open(output_path, "w", encoding="utf8") as handle:
            handle.write(data)

        return output_path

    def __get_decoded_out(self, proc: Popen[bytes]) -> Tuple[str, str]:
        """Gets the decoded stdout and stderr from a Popen call

        Returns:
            Tuple[str, str]: (stdout, stderr) respectively, decoded as strings.
        """
        stdout, stderr = proc.communicate()
        stdout = stdout.decode().replace("\n", " ")
        stderr = stderr.decode().replace("\n", " ")
        return (stdout, stderr)
