from pathlib import Path
from typing import List, Dict


class Renderable:

    def __init__(self):
        self.is_dynamic: bool = None
        self.file_path: Path = None
        self.template_keys: List[str] = None

    def __init__(self, file_path: Path):
        """Alternative constructor for ease of use to pass in the FilePath for a static Renderable

        Args:
            file_path (Path): The Path to the .star file
        """
        self.is_dynamic: bool = False
        self.file_path: Path = file_path
        self.template_keys: List[str] = None

    def resolve_template_keys(self) -> Dict[str, str]:
        """Should be called before rendering to ensure the data rendered is up to date

        Returns:
            Dict[str, str]: A mapping of template keys to their most up-to-date values
        """
        raise Exception("Default implementation is not supported!")
