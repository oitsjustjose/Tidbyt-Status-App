"""A wrapper class for Config"""

import json

from util import rel_to_abspath


class Config:
    """A cheap JSON-based config reader"""

    def __init__(self, conf_path=rel_to_abspath("../modules.json")) -> None:
        with open(conf_path, "r", encoding="utf-8") as fhandle:
            self.data = json.loads(fhandle.read())

    def get_option(self, option: str) -> bool:
        """Gets a given option, returning False if the option was not defined"""
        return self.data[option] if option in self.data else False

    def get_all(self) -> dict:
        """Gets all the options available as a dict"""
        return self.data
