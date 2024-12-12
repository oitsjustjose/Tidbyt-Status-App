from enum import Enum


class AppState(Enum):
    IDLE = 0
    MEETING = 1
    OBS_PAUSED = 2
    OBS_RECORDING = 3
    OBS_STREAMING = 4
