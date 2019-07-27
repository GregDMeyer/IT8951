
from PIL import Image, ImageDraw, ImageFont
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
    epd.clear()

def display_gradient(epd):
    print('Displaying gradient...')

    # set frame buffer to gradient
    for i in range(16):
        epd.frame_buf.paste(i*0x10, box=(i*epd.width//16, 0, (i+1)*epd.width//16, epd.height))

    # update display
    epd.write_full(constants.DisplayModes.GC16)

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

    epd.write_full(constants.DisplayModes.GC16)

def place_text(img, text, x_offset=0, y_offset=0):
    '''
    Put some centered text at a location on the image.
    '''
    fontsize = 80

    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSans.ttf', fontsize)

    img_width, img_height = img.size
    text_width, _ = font.getsize(text)
    text_height = fontsize

    draw_x = (img_width - text_width)//2 + x_offset
    draw_y = (img_height - text_height)//2 + y_offset

    draw.text((draw_x, draw_y), text, font=font)

def partial_update(epd):
    print('Starting partial update...')

    # clear image to white
    epd.frame_buf.paste(0xFF, box=(0, 0, epd.width, epd.height))

    print('  writing full...')
    place_text(epd.frame_buf, 'partial', x_offset=-200)
    epd.write_full(constants.DisplayModes.GC16)

    # TODO: should use 1bpp for partial text update
    print('  writing partial...')
    place_text(epd.frame_buf, 'update', x_offset=+200)
    epd.write_partial(constants.DisplayModes.DU)

def main():
    print('Initializing EPD...')
    epd = EPD(vcom=-2.06)
    print('VCOM set to', epd.get_vcom())

    tests = [
        print_system_info,
        clear_display,
        display_gradient,
        partial_update,
        display_image_8bpp,
    ]

    for t in tests:
        t(epd)
        sleep(1)

    print('Done!')

if __name__ == '__main__':
    main()
