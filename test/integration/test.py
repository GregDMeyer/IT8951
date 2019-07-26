
from PIL import Image
import numpy as np
from time import sleep

from sys import path
path += ['../../']
from IT8951 import EPD, constants

def print_system_info(epd):
    print('System info:')
    print('  display size: {}x{}'.format(epd.width, epd.height))
    print('  img buffer address: {:X}'.format(epd.img_buf_address))
    print('  firmware version: {}'.format(epd.firmware_version))
    print('  LUT version: {}'.format(epd.lut_version))
    print()

def clear_display(epd):
    print('Clearing display...')

    # set frame buffer to all white
    epd.frame_buf.paste(0xFF, box=(0, 0, epd.width, epd.height))

    # load image to controller
    epd.wait_display_ready()
    epd.packed_pixel_write(
        constants.EndianTypes.LITTLE,
        constants.PixelModes.M_8BPP,
        constants.Rotate.NONE,
    )

    # display loaded image, using mode 0 (init)
    epd.display_area(
        (0, 0),
        (epd.width, epd.height),
        constants.WaveformModes.INIT
    )

    sleep(1)

def display_black(epd):
    print('Displaying black...')

    # set frame buffer to all black
    epd.frame_buf.paste(0x00, box=(0, 0, epd.width, epd.height))

    # load image to controller
    epd.wait_display_ready()
    epd.packed_pixel_write(
        constants.EndianTypes.LITTLE,
        constants.PixelModes.M_8BPP,
        constants.Rotate.NONE,
        (0, 0),
        (epd.width, epd.height)
    )

    # display loaded image
    epd.display_area(
        (0, 0),
        (epd.width, epd.height),
        constants.WaveformModes.GC16
    )

    sleep(1)

def display_image_8bpp(epd):
    img_path = 'images/sleeping_penguin.png'
    print('Displaying "{}"...'.format(img_path))

    # clearing image to white
    epd.frame_buf.paste(0xFF, box=(0, 0, epd.width, epd.height))

    img = Image.open(img_path)

    # TODO: this should be built-in
    dims = (epd.width, epd.height)
    img.thumbnail(dims)
    paste_coords = [dims[i] - img.size[i] for i in (0,1)]  # align image with bottom of display
    epd.frame_buf.paste(img, paste_coords)

    # load image to controller
    epd.wait_display_ready()
    epd.packed_pixel_write(
        constants.EndianTypes.LITTLE,
        constants.PixelModes.M_8BPP,
        constants.Rotate.NONE,
    )

    # display loaded image, using mode 0 (init)
    epd.display_area(
        (0, 0),
        (epd.width, epd.height),
        constants.WaveformModes.GC16
    )

    sleep(1)

def main():
    print('Initializing EPD...')
    epd = EPD(vcom=-2.06)
    print('VCOM set to', epd.get_vcom())

    print_system_info(epd)
    clear_display(epd)
    display_black(epd)
    display_image_8bpp(epd)

    print('Done!')

if __name__ == '__main__':
    main()
