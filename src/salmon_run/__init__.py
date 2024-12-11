"""All about Splatoon Salmon Run rendering"""

from dataclasses import dataclass
from datetime import datetime
from time import sleep
from typing import List, Union

import dateutil.parser
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import pixlet
from salmon_run.images import loadout_to_b64
from util import Renderable, rel_to_abspath


@dataclass
class SalmonRunEvent:
    """Represents a GrizzCo Job"""

    start: datetime
    end: datetime
    stage_name: str
    loadout: List[str]


@dataclass
class Cache:
    """Caching System"""

    last_update: datetime
    event: list


class SalmonRunRenderer(Renderable):
    """The class-instanced renderer for splatoon, including a little renderer cache"""

    def __init__(self) -> None:
        self.cache: Union[Cache, None] = None
        self.render_file = rel_to_abspath("../templates/rendered.star")
        self.pixlet_out = self.render_file.replace(".star", ".webp")

    def render(self) -> None:
        """
        Renders out the Splatoon module
        Arguments: None
        Returns: None
        """
        if (
            self.cache
            and self.cache.last_update.date() == datetime.datetime.now().date()
        ):
            pixlet.display(self.pixlet_out, installation_id="status")
            return

        data = self.__get_salmon_run_data()[0]
        pixlet.update_template(
            rel_to_abspath("../templates/splatoon.star"),
            self.render_file,
            {
                "<IMAGE>": loadout_to_b64(data.loadout),
                "<START_DATE>": f"{data.start.month}/{data.start.day} {data.start.hour%12}:{str(data.start.minute).zfill(2)} {'AM' if data.start.hour < 12 else 'PM'}",
                "<END_DATE>": f"{data.end.month}/{data.end.day} {data.end.hour%12}:{str(data.end.minute).zfill(2)} {'AM' if data.end.hour < 12 else 'PM'}",
                "<STAGE>": data.stage_name,
            },
        )
        pixlet.render(self.render_file)
        pixlet.display(self.pixlet_out, installation_id="status")
        sleep(60)

    def __get_salmon_run_data(self) -> List[SalmonRunEvent]:
        """
        Scrapes salmon run data
        Arguments: None
        Returns: (List[SalmonRunEvent]): a list of all salmon run events upcoming
        """

        if (
            self.cache
            and self.cache.last_update.date() == datetime.datetime.now().date()
        ):
            return self.cache.event

        options = Options()
        options.add_argument("--headless")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )
        driver.get("https://splatoon.oatmealdome.me/three/salmon-run")

        main_el = driver.page_source
        main_el = BeautifulSoup(main_el, features="html.parser")
        main_el = main_el.body.find("main").find("div", attrs={"class": "d-grid gap-3"})

        # The row where the datetime is shown when the evt. will occur
        times: List[str] = [
            x.text.strip()
            for x in main_el.find_all("div", attrs={"class": "d-flex flex-row"})
        ]
        # The row where the actual Salmon Run loadout & reward is
        events: List[BeautifulSoup] = main_el.find_all(
            "div", attrs={"class": "bg-salmon-run"}
        )

        data: List[SalmonRunEvent] = []

        for idx, evt in enumerate(events):
            start, end = times[idx].split(" - ")
            start = dateutil.parser.parse(start)
            end = dateutil.parser.parse(end)
            stage_name = evt.find("span", attrs={"class": "text-stage-name"}).text

            event_root = evt.find("div", attrs={"class": "col d-flex flex-column"})

            # Get the photos of the loadout, then lean on the `title` attr
            loadout = [
                f"https://splatoon.oatmealdome.me/{x.find('img').attrs['src']}"
                for x in event_root.find("div", attrs={"class": "row gx-2"}).find_all(
                    "picture"
                )
            ]

            data.append(SalmonRunEvent(start, end, stage_name, loadout))

        driver.close()
        self.cache = Cache(last_update=datetime.datetime.now(), event=data)
        return data
