"""General image magiks"""
import base64
import os
from typing import List

import requests
from PIL import Image
from webptools import dwebp

from util import rel_to_abspath


def download_image(link: str) -> str:
    """Downloads an image via url only if it doesn't exist locally"""
    out_dir = rel_to_abspath("../weapons").replace("\\", os.sep).replace("/", os.sep)
    file_name = link.split("/")[-1]
    full_path = f"{out_dir}/{file_name}".replace("\\", os.sep).replace("/", os.sep)

    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    if not os.path.exists(full_path):
        img_data = requests.get(link).content
        with open(full_path, "wb") as handler:
            handler.write(img_data)

    return full_path


def loadout_to_b64(loadout: List[str]) -> str:
    """
    Converts a list of URLs to webp images (of each loadout) into one,
        24x24 composite rotating webp as base64
    Arguments:
        loadout (List[str]): a list of URLs for each weapon
    """
    frames: List[Image.Image] = []
    for img_url in loadout:
        path = download_image(img_url)
        # Convert webp to png
        dwebp(input_image=path, output_image=f"{path}.png", option="-o")
        frames.append(Image.open(path).resize((24, 24)))

    gif_path = rel_to_abspath("../temp.gif")
    frames[0].save(
        gif_path,
        format="GIF",
        append_images=frames[1:],
        save_all=True,
        duration=5000,
        disposal=2,
        loop=0,
    )

    with open(gif_path, "rb") as fh:
        b64 = base64.b64encode(fh.read())
    os.unlink(gif_path)
    return b64.decode("utf-8")
