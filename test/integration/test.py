
from IT8951 import EPD

def print_system_info(epd):
    print('System info:')
    print('  display size: {}x{}'.format(epd.width, epd.height))
    print('  img buffer address: {:X}'.format(epd.img_buf_address))
    print('  firmware version: {}'.format(epd.firmware_version))
    print('  LUT version: {}'.format(epd.lut_version))
    print()

def main():
    print('Initializing EPD...')
    print()
    epd = EPD(vcom=-2.03)

    print_system_info(epd)

    print('Done!')

if __name__ == '__main__':
    main()
