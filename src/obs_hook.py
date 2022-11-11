import json
import os
from util import rel_to_abspath

status = {"STREAMING": False, "RECORDING": False}


def on_event(event):
    if event == obspython.OBS_FRONTEND_EVENT_RECORDING_STARTED:
        status["RECORDING"] = True
        __write()
    if event == obspython.OBS_FRONTEND_EVENT_RECORDING_STOPPED:
        status["RECORDING"] = False
        __write()
    if event == obspython.OBS_FRONTEND_EVENT_STREAMING_STARTED:
        status["STREAMING"] = True
        __write()
    if event == obspython.OBS_FRONTEND_EVENT_STREAMING_STOPPED:
        status["STREAMING"] = False
        __write()


def __write():
    with open(rel_to_abspath("../status"), "w") as fh:
        fh.write(json.dumps(status))


def script_load(settings):
    __write()
    obspython.obs_frontend_add_event_callback(on_event)
