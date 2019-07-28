
from PIL import Image, ImageDraw, ImageFont
import cProfile
import pstats
import io

from sys import path
path += ['../../']
from IT8951 import EPD, constants

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

def profile_func(f, *args, sortby='cumulative', **kwargs):
    pr = cProfile.Profile()
    pr.enable()
    f(*args, **kwargs)
    pr.disable()
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print(s.getvalue())

def main():
    print('Initializing...')
    epd = EPD(vcom=-2.06)
    epd.clear()

    print('Writing initial image...')
    place_text(epd.frame_buf, 'partial', x_offset=-200)
    epd.write_full(constants.DisplayModes.GC16)

    # so that we're not timing the previous operations
    epd.wait_display_ready()

    print('Doing partial update...')
    place_text(epd.frame_buf, 'update', x_offset=+200)
    profile_func(
        epd.write_partial,
        constants.DisplayModes.GL16   # should see what best mode is here
    )

if __name__ == '__main__':
    main()
