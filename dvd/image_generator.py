from pathlib import Path
from random import randint
from typing import Tuple

from PIL import Image, ImageChops

def rgb_to_hsl(color: Tuple[int, int, int]) -> Tuple[None, None, float]:
    _r = color[0] / 255
    _g = color[1] / 255
    _b = color[2] / 255
    c_max = max(_r, _g, _b)
    c_min = min(_r, _g, _b)
    l = (c_max + c_min) / 2
    return (None, None, l)

def generate_random_color_dvd_logo(dvd_logo: Image) -> Image.Image:
    hsl = (0, 0, 0)
    while hsl[2] < 0.5:
        color = (
            randint(100, 255),
            randint(100, 255),
            randint(100, 255),
            255
        )
        hsl = rgb_to_hsl(color)

    color_img = Image.new('RGBA', (dvd_logo.width, dvd_logo.height), color)
    return ImageChops.multiply(color_img, dvd_logo)

def generate_frame(
    position: Tuple[float, float],
    resolution: Tuple[float, float],
    dvd_logo: Image.Image,
    dvd_logo_color: Image.Image,
) -> Image.Image:
    frame = Image.new('RGBA', resolution, '#000000FF')
    frame.paste(dvd_logo_color,
                position,
                mask=dvd_logo)
    return frame

def get_scaled_dvd_logo(scale: float, scl: float) -> Image.Image:
    this_path = Path(__file__)
    logo_path = this_path.parent / Path('dvd_logo.png')
    dvd_logo = Image.open(logo_path)
    ratio = scale * scl / 1.5
    new_logo_size = (int(dvd_logo.width / ratio), int(dvd_logo.height / ratio))
    return dvd_logo.resize(new_logo_size, Image.LANCZOS)
