#!/usr/bin/python

from PIL import Image
from PIL.ImageOps import mirror, flip


def reflect_image(source, reflection_mode):
    """Reflect a pillow Image object to create symmetric image

    Parameters
    ----------
    source : PIL.Image
        Source image that will be reflected
    reflection_mode : string
        Reflection based on compass orientation in lower case.
        (e.g. "e", "n", "sw')

    Returns
    -------
    PIL.Image
        Image object from reflected source
    """
    return source


# Image Flipping function
def mirror_top(source):
    crop_height = int(source.height / 2)
    cropped = source.crop((0, 0, source.width, crop_height))
    result = Image.new(source.mode, (source.width, 2 * crop_height))
    result.paste(cropped, (0, 0))
    result.paste(flip(cropped), (0, cropped.height))
    return result


def mirror_bottom(source):
    crop_height = int(source.height / 2)
    cropped = source.crop((0, crop_height, source.width, 2 * crop_height))
    result = Image.new(source.mode, (source.width, 2 * crop_height))
    result.paste(flip(cropped), (0, 0))
    result.paste(cropped, (0, cropped.height))
    return result


def mirror_left(source):
    crop_width = int(source.width / 2)
    cropped = source.crop((0, 0, crop_width, source.height))
    result = Image.new(source.mode, (2 * crop_width, source.height))
    result.paste(cropped, (0, 0))
    result.paste(mirror(cropped), (cropped.width, 0))
    return result


def mirror_right(source):
    crop_width = int(source.width / 2)
    cropped = source.crop((crop_width, 0, 2 * crop_width, source.height))
    result = Image.new(source.mode, (2 * crop_width, source.height))
    result.paste(mirror(cropped), (0, 0))
    result.paste(cropped, (cropped.width, 0))
    return result
