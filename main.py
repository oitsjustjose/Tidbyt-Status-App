import json
import os
import subprocess
from dynamic_star import show_text
from time import sleep
from typing import List
from dataclasses import dataclass
from bs4 import BeautifulSoup
from pywinauto import Desktop
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

path_root = os.path.realpath(__file__).replace("main.py", "")


@dataclass
class SalmonRunEvent:
    date: str
    stage_name: str
    loadout: str
    rewards: str


def abp(path: str) -> str:
    return f"{path_root}\\{path}"


def display(file_name: str):
    with open(abp("device_id"), "r", encoding="utf-8") as file_handle:
        device_id = file_handle.read()
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    subprocess.Popen(
        [abp("pixlet.exe"), "push", device_id, abp(file_name)], startupinfo=startupinfo
    ).wait()


def get_salmon_run_data() -> List[SalmonRunEvent]:
    """Scrapes salmon run data"""
    options = Options()
    options.add_argument("--headless")

    driver = webdriver.Firefox(options=options)
    driver.get("https://splatoon.oatmealdome.me/three/salmon-run")

    page_source = driver.page_source
    page_source = BeautifulSoup(page_source, features="html.parser")
    main_entry = page_source.body.find("main", attrs={"role": "main"}).find(
        "div", attrs={"class": "d-grid gap-3"}
    )

    # The row where the datetime is shown when the evt. will occur
    times = [
        x.text.strip()
        for x in main_entry.find_all("div", attrs={"class": "d-flex flex-row"})
    ]
    # The row where the actual Salmon Run loadout & reward is
    events: List[BeautifulSoup] = main_entry.find_all(
        "div", attrs={"class": "bg-salmon-run"}
    )

    data = []

    for idx, evt in enumerate(events):
        time = times[idx]
        stage_name = evt.find("span", attrs={"class": "text-stage-name"}).text

        event_root = evt.find("div", attrs={"class": "col d-flex flex-column"})

        # Get the photos of the loadout, then lean on the `title` attr
        loadout_pic_els = event_root.find("div", attrs={"class": "row gx-2"}).find_all(
            "picture"
        )
        loadout = [x.find("img").attrs["title"] for x in loadout_pic_els]

        # Get the photos of the reward, then lean on the `title` attr
        reward_pic_els = event_root.find(
            "div", attrs={"class": "row mt-3 gx-2"}
        ).find_all("picture")
        rewards = [x.find("img").attrs["title"] for x in reward_pic_els]

        data.append(
            SalmonRunEvent(time, stage_name, ", ".join(loadout), ", ".join(rewards))
        )

    driver.close()
    return data


def main():
    desktop = Desktop()

    salmon_runs = get_salmon_run_data()
    text = []
    for event in salmon_runs:
        # Display the event for a bit, then sleep
        text.append(
            f"""{event.date}\n\nSTAGE:\n{event.stage_name}\n\nLOADOUT:\n{event.loadout}\n\nREWARD(S):\n{event.rewards}"""
        )
        # show_text(
        #     f"{event.date}: {event.stage_name}",
        #     f"Loadout: {event.loadout} | Rewards: {event.rewards}",
        # )
        # sleep(60)

    show_text("\n-------\n\n".join(text))
    return

    # print(json.dumps(get_salmon_run_data(), indent=2))
    # return
    while True:
        try:
            windows = list(
                filter(lambda x: x, [w.window_text() for w in desktop.windows()])
            )

            if "Zoom Meeting" in windows:
                display("zoom/meeting.webp")
                sleep(16)
            elif "obs64" in windows:
                with open(abp("status"), "r", encoding="utf-8") as file_handle:
                    data = json.loads(file_handle.read())
                    if data["STREAMING"]:
                        display("streaming/active.webp")
                        sleep(10)
                    elif data["RECORDING"]:
                        display("recording/active.webp")
                        sleep(12)
                    else:
                        display("recording/paused.webp")
                        sleep(10)
            else:
                sleep(1)
        except KeyboardInterrupt:
            print("Quitting...")
            break


main()
