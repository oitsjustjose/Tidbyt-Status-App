import base64
import os
from typing import List, Tuple

import requests
from PIL import Image
from webptools import cwebp, dwebp, webpmux_animate

from util import rel_to_abspath


def download_image(link: str) -> Tuple[bool, str]:
    """Downloads an image via url only if it doesn't exist locally"""
    out_dir = rel_to_abspath("../weapons").replace("\\", os.sep).replace("/", os.sep)
    file_name = link.split("/")[-1]
    full_path = f"{out_dir}/{file_name}".replace("\\", os.sep).replace("/", os.sep)

    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    existed = True
    if not os.path.exists(full_path):
        existed = False
        img_data = requests.get(link).content
        with open(full_path, "wb") as handler:
            handler.write(img_data)

    return (existed, full_path)


def loadout_to_b64(loadout: List[str]) -> str:
    """
    Converts a list of URLs to webp images (of each loadout) into one,
        24x24 composite rotating webp as base64
    Arguments:
        loadout (List[str]): a list of URLs for each weapon
    """
    inputs: List[str] = []
    for img_url in loadout:
        existed, path = download_image(img_url)
        if not existed:  # Only resize if the image didn't already exist
            dwebp(input_image=path, output_image=f"{path}.png", option="-o")
            Image.open(f"{path}.png").resize((24, 24)).save(f"{path}.png")
            cwebp(input_image=f"{path}.png", output_image=path, option="-q 100")
            os.unlink(f"{path}.png")
        inputs.append(f"{path} +1000+0+0+1")

    webpmux_animate(
        input_images=inputs,
        output_image=rel_to_abspath("../temp.webp"),
        loop="10",
        bgcolor="0,0,0,0",
    )

    img = Image.open(rel_to_abspath("../temp.webp"))
    img.info.pop("background", None)
    img.save(rel_to_abspath("../temp.gif"), "gif", save_all=True)

    with open(rel_to_abspath("../temp.gif"), "rb") as file_handle:
        b64 = base64.b64encode(file_handle.read())
    # os.unlink(rel_to_abspath("../temp.webp"))
    return b64


print(
    loadout_to_b64(
        [
            "https://splatoon.oatmealdome.me/img/weapon/thunder/Shooter_Short_00.webp",
            "https://splatoon.oatmealdome.me/img/weapon/thunder/Blaster_Short_00.webp",
            "https://splatoon.oatmealdome.me/img/weapon/thunder/Shelter_Compact_00.webp",
            "https://splatoon.oatmealdome.me/img/weapon/thunder/Charger_Normal_00.webp",
        ]
    )
)
