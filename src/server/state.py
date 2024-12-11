from enum import Enum
from pathlib import Path
from threading import Thread
from time import sleep
from typing import Dict

from pixlet import push_to_tidbyt
from renderables import Renderable
from renderables.forgeserv import ForgeServ


class AppState(Enum):
    IDLE = 0
    MEETING = 1
    OBS_PAUSED = 2
    OBS_RECORDING = 3
    OBS_STREAMING = 4


ROOT = Path("./")


class StateManager:
    def __init__(self, timeout=1):
        """Manages the state of the Tidbyt manager application

        Args:
            timeout (int, optional): How long to wait between iterations (in seconds). Defaults to 1.
        """
        self.state: AppState = AppState.IDLE
        self.renderables: Dict[AppState, Renderable] = {
            AppState.IDLE: ForgeServ(),
            AppState.MEETING: Renderable(
                ROOT.joinpath("templates/meeting.star").resolve()
            ),
            AppState.OBS_PAUSED: Renderable(
                ROOT.joinpath("templates/obs/paused.star").resolve()
            ),
            AppState.OBS_RECORDING: Renderable(
                ROOT.joinpath("templates/obs/recording.star").resolve()
            ),
            AppState.OBS_STREAMING: Renderable(
                ROOT.joinpath("templates/obs/streaming.star").resolve()
            ),
        }
        # Thread related activities & vars
        self.timeout = timeout
        self.thread: Thread = None
        self.stop_thread = False
        self.__start()

    def update(self, new_state: AppState):
        """Update the Tidbyt's state, returning the prior state

        Args:
            new_state (AppState): The new application state
        """
        if self.state == new_state:
            return self.state

        self.state = new_state
        push_to_tidbyt(self.renderables[self.state])

    def __start(self):
        """Instantiates and starts the worker thread

        Raises:
            Exception: thrown if the thread has already been instantiated
        """
        if self.thread:
            raise Exception("Thread has already been initialized!")
        self.thread = Thread(target=self.__thread_task, daemon=True)
        self.thread.start()

    def __thread_task(self):
        """A looping task that renders and pushes the correct pixlet based on state"""
        while not self.stop_thread:
            if self.renderables[self.state].is_dynamic:
                push_to_tidbyt(self.renderables[self.state])
            sleep(self.timeout)