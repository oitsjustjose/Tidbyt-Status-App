import logging
from pathlib import Path
from threading import Thread
from time import sleep
from typing import Dict

from common.appstate import AppState
from server.pixlet import PixletHelper
from server.renderables import Renderable
from server.renderables.forgeserv import ForgeServ


class StateManager:
    def __init__(self, timeout=1):
        """Manages the state of the Tidbyt manager application

        Args:
            timeout (int, optional): How long to wait between iterations (in seconds). Defaults to 1.
        """
        self.logger = logging.getLogger("uvicorn.error")
        self.state: AppState = AppState.IDLE
        self.renderables: Dict[AppState, Renderable] = {
            AppState.IDLE: ForgeServ(),
            AppState.MEETING: Renderable(Path("./templates/meeting.star").resolve()),
            AppState.OBS_PAUSED: Renderable(
                Path("./templates/obs/paused.star").resolve()
            ),
            AppState.OBS_RECORDING: Renderable(
                Path("./templates/obs/recording.star").resolve()
            ),
            AppState.OBS_STREAMING: Renderable(
                Path("./templates/obs/streaming.star").resolve()
            ),
        }
        # Thread related activities & vars
        self.timeout = timeout
        self.thread: Thread = None
        self.stop_thread = False
        self.__pixlet_helper = PixletHelper()

    def update(self, new_state: AppState):
        """Update the Tidbyt's state, returning the prior state

        Args:
            new_state (AppState): The new application state
        """
        if self.state == new_state:
            return self.state

        self.state = new_state
        self.__pixlet_helper.push_to_tidbyt(self.renderables[self.state])

    def start(self):
        """Instantiates and starts the worker thread

        Raises:
            Exception: thrown if the thread has already been instantiated
        """
        if self.thread:
            raise Exception("Thread has already been initialized!")
        self.thread = Thread(target=self.__thread_task, daemon=True)
        self.thread.start()
        self.logger.info(f"Started thread with tid={self.thread.ident}")

    def __thread_task(self):
        """A looping task that renders and pushes the correct pixlet based on state"""
        while not self.stop_thread:
            try:
                if self.renderables[self.state].is_dynamic:
                    self.__pixlet_helper.push_to_tidbyt(self.renderables[self.state])
                sleep(self.timeout)
            except Exception as e:
                self.logger.warning(
                    f"Thread task ran into an {type(e).__name__}: {str(e)}"
                )
                sleep(self.timeout * 2)
