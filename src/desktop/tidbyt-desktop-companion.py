import urllib.request
from os import getenv
from time import sleep
from typing import List

import win32gui
import win32process
from wmi import WMI

from src.common.appstate import AppState


class MeetingWindow:
    def __init__(self, exec_name: str, title_part: str):
        """A window with a given executable and window title

        Args:
            exec_name (str): The name of the executable
            title_part (str): The string used to determine if the window title is a match
        """
        self.__exec_name: str = exec_name.lower()
        self.__title_part: str = title_part.lower()

    def matches_title(self, other: str) -> bool:
        """Determines if the passed in window title contains the title part of this object

        Args:
            other (str): The window title to test against

        Returns:
            bool: True if the title matches at all, false otherwise
        """
        return self.__title_part in other.lower()

    def matches_executable(self, other: str) -> bool:
        """Determines if the passed in executable matches the executable defined in this object

        Args:
            other (str): The name of the executable of the other executable

        Returns:
            bool: True if the name of the executables match (ignoring case), false otherwise
        """
        return self.__exec_name == other.lower()

    def __str__(self):
        return f"[{self.__exec_name}]: '{self.__title_part}'"


class Main:
    def __init__(self, sleep_intvl=2):
        """The main class that stores state across all of the various methods

        Args:
            sleep_intvl (int, optional): How long to sleep between iters. Defaults to 2.
        """
        self.__found_meeting = False
        self.__last_state = AppState.IDLE

        self.__wmi = WMI()
        self.__sleep_intvl = sleep_intvl
        self.__backend_uri = getenv("TIDBYT_SERVER_URI", "http://172.16.1.6:8000")
        self.__meeting_windows = [
            MeetingWindow("slack.exe", "Huddle"),
            MeetingWindow("Zoom.exe", "Zoom Meeting"),
        ]

    def run(self) -> None:
        while True:
            try:
                self.__found_meeting = False
                win32gui.EnumWindows(self.__win_enum_handler, None)

                new_state = AppState.MEETING if self.__found_meeting else AppState.IDLE
                if new_state != self.__last_state:
                    self.__set_state(new_state)
                    self.__last_state = new_state

                print(self.__found_meeting)

                sleep(self.__sleep_intvl)
            except KeyboardInterrupt:
                break
            except:
                pass

    def __set_state(self, state: AppState) -> None:
        """Helper method to quickly set the TidByt's state via REST in a single small method call

        Args:
            state (AppState): The new meeting state
        """
        urllib.request.urlopen(f"{self.__backend_uri}?new_state={state.value}", data={})

    def __win_enum_handler(self, hwnd: int, _: None) -> bool:
        """_summary_

        Args:
            hwnd (int): The window handle ID from the enumerator
            _ (None): Extra packed in params (unused)

        Returns:
            bool: True if the enumerator should continue (i.e. hasn't found a match), False to stop (match found)
        """
        win_title = win32gui.GetWindowText(hwnd)

        matches: List[MeetingWindow] = list(filter(lambda x: x.matches_title(win_title), self.__meeting_windows))

        if not matches:
            return True

        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        rows = self.__wmi.query(f"SELECT Name FROM Win32_Process WHERE ProcessId = {pid}")

        if not any([x.matches_executable(y.Name) for x in matches for y in rows]):
            return True

        self.__found_meeting = True
        return False


if __name__ == "__main__":
    Main().run()
