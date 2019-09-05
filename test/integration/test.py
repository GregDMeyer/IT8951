
from time import sleep
import argparse

from test_functions import *

def parse_args():
    p = argparse.ArgumentParser(description='Test EPD functionality')
    p.add_argument('-v', '--virtual', action='store_true',
                   help='display using a Tkinter window instead of the '
                        'actual e-paper device (for testing without a '
                        'physical device)')
    return p.parse_args()
    
def main():

    args = parse_args()

    from sys import path
    path += ['../../']

    tests = []
    
    if not args.virtual:
        from IT8951.display import AutoEPDDisplay

        print('Initializing EPD...')
        display = AutoEPDDisplay(vcom=-2.06)
        print('VCOM set to', display.epd.get_vcom())

        tests += [print_system_info]
        
    else:
        from IT8951.display import VirtualEPDDisplay
        display = VirtualEPDDisplay(dims=(800, 600))
        
    tests += [
        clear_display,
        display_gradient,
        partial_update,
        display_image_8bpp,
    ]

    for t in tests:
        t(display)
        sleep(1)

    print('Done!')

if __name__ == '__main__':
    main()
