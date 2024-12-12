import urllib.request
from os import getenv

from src.common.appstate import AppState


def on_event(event):
    state: AppState = AppState.IDLE
    backend_uri = getenv("TIDBYT_SERVER_URI", "http://172.16.1.6:8000")

    if event == obspython.OBS_FRONTEND_EVENT_RECORDING_STARTED:
        state = AppState.OBS_RECORDING
    elif event == obspython.OBS_FRONTEND_EVENT_STREAMING_STARTED:
        state = AppState.OBS_STREAMING
    elif (
        event == obspython.OBS_FRONTEND_EVENT_RECORDING_STOPPED
        or event == obspython.OBS_FRONTEND_EVENT_STREAMING_STOPPED
    ):
        state = AppState.OBS_PAUSED

    urllib.request.urlopen(f"{backend_uri}?new_state={state.value}", data={})


def script_load(_):
    obspython.obs_frontend_add_event_callback(on_event)


def script_unload():
    backend_uri = getenv("TIDBYT_SERVER_URI", "http://172.16.1.6:8000")

    urllib.request.urlopen(f"{backend_uri}?new_state={AppState.IDLE.value}", data={})
