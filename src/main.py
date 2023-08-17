"""The mainfile"""
import json
import traceback
from dataclasses import dataclass
from time import sleep
from typing import Dict

from pywinauto import Desktop
from pywinauto.controls.hwndwrapper import InvalidWindowHandle

import pixlet
from config import Config
from forgeserv import ForgeServRenderer
from salmon_run import SalmonRunRenderer
from util import Renderable, rel_to_abspath


@dataclass
class RenderType:
    """A list of all various render types"""

    HUDDLE = "HUDDLE"
    OBS_PAUSED = "OBS_PAUSED"
    OBS_RECORDING = "OBS_RECORDING"
    OBS_STREAMING = "OBS_STREAMING"
    SPLATOON = "SPLATOON"
    FORGESERV = "FORGESERV"
    ZOOM = "ZOOM"


def main():
    """The main run function of the application"""
    desktop = Desktop()
    config = Config()
    rendering = ""

    renderers: Dict[str, Renderable] = {
        RenderType.SPLATOON: SalmonRunRenderer(),
        RenderType.FORGESERV: ForgeServRenderer(),
    }

    while True:
        try:
            windows = list(
                filter(
                    lambda x: x,  # Filter out empty vals
                    [w.window_text() for w in desktop.windows()],
                )
            )

            huddle_windows = list(filter(lambda x: "huddle" in x.lower(), windows))
            obs_windows = list(
                filter(lambda x: "obs" in x.lower() and "64" in x.lower(), windows)
            )

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
                print("e")
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
                if config.get_option("splatoon"):
                    # If the uploaded render isn't already splatoon, push it
                    if rendering != RenderType.SPLATOON:
                        rendering = RenderType.SPLATOON
                elif config.get_option("forgeserv"):
                    if rendering != RenderType.FORGESERV:
                        rendering = RenderType.FORGESERV
                renderers[rendering].render()

        except KeyboardInterrupt:
            break
        except InvalidWindowHandle:
            continue
        except Exception as ex:
            with open(
                rel_to_abspath("../out.log"), "a+", encoding="utf-8"
            ) as log_handle:
                log_handle.write(f"{ex}\n")
                tb_lines = [
                    line.rstrip("\n")
                    for line in traceback.format_exception(
                        ex.__class__, ex, ex.__traceback__
                    )
                ]

                _ = [log_handle.write(f"{x}\n") for x in tb_lines]
        sleep(1)


if __name__ == "__main__":
    with open(rel_to_abspath("../out.log"), "w", encoding="utf-8") as log_handle:
        log_handle.write("")
    main()
