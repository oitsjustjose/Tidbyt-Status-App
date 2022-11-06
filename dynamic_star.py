import os
import subprocess

STARTUP_INFO = subprocess.STARTUPINFO()
STARTUP_INFO.dwFlags |= subprocess.STARTF_USESHOWWINDOW

TEMPLATE = '''
load("render.star", "render")
load("encoding/base64.star", "base64")

def main():
    return render.Root(
        max_age=60,
        delay=125,
        child=render.Marquee(
            height=32,
            offset_start = 32,
            offset_end = 32,
            scroll_direction="vertical",
            child=render.WrappedText("""<TEMP>""", width=60)
        )
    )
'''


def _abp(path: str) -> str:
    path_root = os.path.realpath(__file__).replace("dynamic_star.py", "")
    return f"{path_root}\\{path}"


def _render():
    subprocess.Popen(
        [_abp("pixlet.exe"), "render", _abp("splatoon_dynamic.star")],
        startupinfo=STARTUP_INFO,
    ).wait()


def _display():
    with open(_abp("device_id"), "r", encoding="utf-8") as file_handle:
        device_id = file_handle.read()
    subprocess.Popen(
        [
            _abp("pixlet.exe"),
            "push",
            "--installation-id",
            "SalmonRun",
            device_id,
            _abp("splatoon_dynamic.webp"),
        ],
        startupinfo=STARTUP_INFO,
    ).wait()


def show_text(text: str) -> None:
    with open(_abp("splatoon_dynamic.star"), "w", encoding="utf-8") as file_handle:
        file_handle.write(TEMPLATE.replace("<TEMP>", text))
    _render()
    _display()
