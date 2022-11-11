"""The mainfile"""
import json
from dataclasses import dataclass
from datetime import datetime
from time import sleep
from typing import List

import dateutil.parser
from bs4 import BeautifulSoup
from pywinauto import Desktop
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import pixlet
from images import loadout_to_b64
from util import rel_to_abspath


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
    event: List[SalmonRunEvent]


CACHED: Cache = None


def get_salmon_run_data() -> List[SalmonRunEvent]:
    """Scrapes salmon run data"""
    global CACHED
    if CACHED and CACHED.last_update.date() == datetime.now().date():
        return CACHED.event

    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get("https://splatoon.oatmealdome.me/three/salmon-run")

    main_el = driver.page_source
    main_el = BeautifulSoup(main_el, features="html.parser")
    main_el = main_el.body.find("main", attrs={"role": "main"}).find(
        "div", attrs={"class": "d-grid gap-3"}
    )

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
    CACHED = Cache(last_update=datetime.now(), event=data)
    return data


def main():
    """The main run function of the application"""
    desktop = Desktop()
    showing_sploon = False
    rotation_time = 15  # the amount of time between tidbyt app rotations

    while True:
        try:
            windows = list(
                filter(lambda x: x, [w.window_text() for w in desktop.windows()])
            )

            huddle_windows = list(filter(lambda x: "Huddle with" in x, windows))

            if "Zoom Meeting" in windows:
                showing_sploon = False
                pixlet.display(rel_to_abspath("../zoom/meeting.webp"))
                sleep(rotation_time)
            if huddle_windows:
                showing_sploon = False
                pixlet.display(rel_to_abspath("../slack/huddle.webp"))
                sleep(rotation_time)
            elif "obs64" in windows:
                showing_sploon = False
                with open(
                    rel_to_abspath("../status"), "r", encoding="utf-8"
                ) as file_handle:
                    data = json.loads(file_handle.read())
                    if data["STREAMING"]:
                        pixlet.display(rel_to_abspath("../streaming/active.webp"))
                    elif data["RECORDING"]:
                        pixlet.display(rel_to_abspath("../recording/active.webp"))
                    else:
                        pixlet.display(rel_to_abspath("../recording/paused.webp"))
                    sleep(rotation_time)
            else:
                # Only re-render a .star file if the cache should have expired or we hadn't rendered one yet
                if not showing_sploon or (
                    CACHED and CACHED.last_update.date() != datetime.now().date()
                ):  # prevents overworking
                    salmon_run = get_salmon_run_data()[0]

                    render_file = rel_to_abspath("../templates/rendered.star")
                    pixlet.update_template(
                        rel_to_abspath("../templates/splatoon.star"),
                        render_file,
                        {
                            "<IMAGE>": loadout_to_b64(salmon_run.loadout),
                            "<START_DATE>": f"{salmon_run.start.month}/{salmon_run.start.day} {salmon_run.start.hour%12}:{str(salmon_run.start.minute).zfill(2)} {'AM' if salmon_run.start.hour < 12 else 'PM'}",
                            "<END_DATE>": f"{salmon_run.end.month}/{salmon_run.end.day} {salmon_run.end.hour%12}:{str(salmon_run.end.minute).zfill(2)} {'AM' if salmon_run.end.hour < 12 else 'PM'}",
                            "<STAGE>": salmon_run.stage_name,
                        },
                    )
                    pixlet.render(render_file)
                    pixlet.display(
                        render_file.replace(".star", ".webp"),
                        installation_id="SalmonRun",
                    )
                    showing_sploon = True
                sleep(5)
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    main()
