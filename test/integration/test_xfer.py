
from test_functions import print_system_info

from sys import path
path += ['../../']
from IT8951.display import AutoEPDDisplay

display = AutoEPDDisplay(vcom=-2.06)
print('VCOM set to', display.epd.get_vcom())
print_system_info(display)
