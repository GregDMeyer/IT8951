
from PIL import Image

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
    epd.frame_buffer[:] = 0xF0

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

def main():
    print('Initializing EPD...')
    epd = EPD(vcom=-2.06)
    print('VCOM set to', epd.get_vcom())

    print_system_info(epd)

    print('Done!')

if __name__ == '__main__':
    main()
