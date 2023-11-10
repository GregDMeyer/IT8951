# IT8951

This Python 3 module implements a driver for the IT8951 e-paper controller, via SPI.
The driver was developed using the 6-inch e-Paper HAT from Waveshare. It hopefully will work for
other (related) hardware too.

To install, clone the repository, enter the directory and run
```
pip install ./[rpi]
```

(If you are installing on a platform other than Raspberry Pi, omit the `[rpi]`).

Make sure that SPI is enabled by running `raspi-config` and navigating to `Interface Options`→`SPI`.

---

### Examples

To display a bitmap image:

```python
from IT8951.display import AutoEPDDisplay
from IT8951 import constants
from PIL import Image

display = AutoEPDDisplay(vcom=-2.48)

# Make display clear
display.clear()

display.frame_buf.paste(0xFF, box=(0, 0, display.width, display.height))
img = Image.open('IT8951/test/integration/images/sleeping_penguin.png')
dims = (display.width, display.height)
img.thumbnail(dims)

# Align image with bottom of display
paste_coords = [dims[i] - img.size[i] for i in (0,1)]
display.frame_buf.paste(img, paste_coords)

# Display the image
display.draw_full(constants.DisplayModes.GC16)
```

To display a polygon:

```python
import math
from PIL import Image, ImageDraw
from PIL import ImagePath
from IT8951.display import AutoEPDDisplay
from IT8951 import constants

display = AutoEPDDisplay(vcom=-2.48)
display.clear()

dims = (display.width, display.height)1
sides = 6

xy = [
    ((math.cos(th) + 1) * 300,
     (math.sin(th) + 1) * 200)
    for th in [i * (2 * math.pi) / sides for i in range(sides)]
    ]

image = ImagePath.Path(xy).getbbox()
img = Image.new("RGB", dims, "#ffffff")
img1 = ImageDraw.Draw(img)
img1.polygon(xy, fill ="#000000", outline ="blue")

paste_coords = [dims[i] - img.size[i] for i in (0,1)]
display.frame_buf.paste(img, paste_coords)
display.draw_full(constants.DisplayModes.GC16)
```

For some more examples of usage, take a look at the integration tests in [test/integration](test/integration)

### Notes on performance

#### VCOM value

You should try setting different VCOM values and seeing how that affects the performance of your display. Every
one is different. There might be a suggested VCOM value marked on the cable of your display.

#### Data transfer

You might be able to squeeze some extra performance out of the data transfer by increasing the SPI
clock frequency.
The SPI frequency for transferring pixel data is by default set at 24 MHz, which is the maximum
stated in the IT8951 chip spec [here](https://www.waveshare.com/w/upload/1/18/IT8951_D_V0.2.4.3_20170728.pdf)
(page 41).
But, you could try setting higher and seeing if it works anyway.
It is set by passing the `spi_hz` argument to the Display or EPD classes (see example in `tests/integration/tests.py`).

#### Running the code on Linux desktop

You can run this library on desktop Linux distributions (e.g. on Ubuntu) using a "virtual" display, for testing and development. Instead of appearing on a real ePaper device, the contents will be shown in a `TKInter` window on the desktop. For an example, see the integration tests at [test/integration/test.py](https://github.com/GregDMeyer/IT8951/blob/master/test/integration/test.py) when passed the `-v` option.

Windows is curently not supported (the `cython` build will fail because the C code depends on some Linux components). It might work if you use some Linux compatibility layer like `WSL` or `Mingw`.

To do so, simply run

```
pip3 install ./
```

Now you should be able to run the tests with the `-v` flag: `python test.py -v`.

## Contributors

Thanks to the following folks for helping improve the library:

 - @BackSlasher
 - @cetres
 - @azzeloof
 - @matyasf
 - @grob6000
 - @txoof
