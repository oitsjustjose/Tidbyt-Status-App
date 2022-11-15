"""The mainfile"""
import json
from dataclasses import dataclass
from datetime import datetime
from time import sleep
from typing import List

import dateutil.parser
from bs4 import BeautifulSoup
from pywinauto import Desktop
from pywinauto.controls.hwndwrapper import InvalidWindowHandle
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


@dataclass
class RenderType:
    HUDDLE = "HUDDLE"
    OBS_PAUSED = "OBS_PAUSED"
    OBS_RECORDING = "OBS_RECORDING"
    OBS_STREAMING = "OBS_STREAMING"
    SPLATOON = "SPLATOON"
    ZOOM = "ZOOM"


CACHED: Cache = None


def get_salmon_run_data() -> List[SalmonRunEvent]:
    """Scrapes salmon run data"""
    global CACHED
    if CACHED and CACHED.last_update.date() == datetime.now().date():
        return CACHED.event

    options = Options()
    options.add_argument("--headless")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
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
    rendering = ""

    while True:
        try:
            windows = list(
                filter(
                    lambda x: x,  # Filter out empty vals
                    [w.window_text() for w in desktop.windows()],
                )
            )

            huddle_windows = list(filter(lambda x: "huddle" in x.lower(), windows))
            obs_windows = list(filter(lambda x: "obs" in x.lower(), windows))

            if "Zoom Meeting" in windows:
                if rendering != RenderType.ZOOM:
                    pixlet.display(
                        rel_to_abspath("../zoom/meeting.webp"),
                        installation_id="status",
                    )
                    rendering = RenderType.ZOOM
            elif huddle_windows:
                if rendering != RenderType.HUDDLE:
                    pixlet.display(
                        rel_to_abspath("../slack/huddle.webp"),
                        installation_id="status",
                    )
                    rendering = RenderType.HUDDLE
            elif obs_windows:
                with open(
                    rel_to_abspath("../status"), "r", encoding="utf-8"
                ) as file_handle:
                    data = json.loads(file_handle.read())
                    if data["STREAMING"]:
                        if rendering != RenderType.OBS_STREAMING:
                            pixlet.display(
                                rel_to_abspath("../streaming/active.webp"),
                                installation_id="status",
                            )
                            rendering = RenderType.OBS_STREAMING
                    elif data["RECORDING"]:
                        if rendering != RenderType.OBS_RECORDING:
                            pixlet.display(
                                rel_to_abspath("../recording/active.webp"),
                                installation_id="status",
                            )
                            rendering = RenderType.OBS_RECORDING
                    else:
                        if rendering != RenderType.OBS_PAUSED:
                            pixlet.display(
                                rel_to_abspath("../recording/paused.webp"),
                                installation_id="status",
                            )
                            rendering = RenderType.OBS_PAUSED
            else:
                # Only re-render a .star file if the cache should have expired or we hadn't rendered one yet
                if (
                    not CACHED
                    or rendering != RenderType.SPLATOON
                    or (CACHED and CACHED.last_update.date() != datetime.now().date())
                ):  # prevents overworking
                    if rendering != RenderType.SPLATOON:
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
                            installation_id="status",
                        )
                        rendering = RenderType.SPLATOON
                    sleep(1)
        except KeyboardInterrupt:
            break
        except InvalidWindowHandle:
            continue
        sleep(0.5)


if __name__ == "__main__":
    main()
