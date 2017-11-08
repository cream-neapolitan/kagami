#!/usr/bin/python

from PIL import Image
from PIL.ImageOps import mirror, flip

# Process incoming Image with specified reflection
def reflect_image(ori, reflection_mode):
    return ori


# Image Flipping function
def mirror_top(ori):
    crop_height = int(ori.height / 2)
    cropped = ori.crop((0, 0, ori.width, crop_height))
    result = Image.new(ori.mode, (ori.width, 2 * crop_height))
    result.paste(cropped, (0, 0))
    result.paste(flip(cropped), (0, cropped.height))
    return result


def mirror_bottom(ori):
    crop_height = int(ori.height / 2)
    cropped = ori.crop((0, crop_height, ori.width, 2 * crop_height))
    result = Image.new(ori.mode, (ori.width, 2 * crop_height))
    result.paste(flip(cropped), (0, 0))
    result.paste(cropped, (0, cropped.height))
    return result


def mirror_left(ori):
    crop_width = int(ori.width / 2)
    cropped = ori.crop((0, 0, crop_width, ori.height))
    result = Image.new(ori.mode, (2 * crop_width, ori.height))
    result.paste(cropped, (0, 0))
    result.paste(mirror(cropped), (cropped.width, 0))
    return result


def mirror_right(ori):
    crop_width = int(ori.width / 2)
    cropped = ori.crop((crop_width, 0, 2 * crop_width, ori.height))
    result = Image.new(ori.mode, (2 * crop_width, ori.height))
    result.paste(mirror(cropped), (0, 0))
    result.paste(cropped, (cropped.width, 0))
    return result
