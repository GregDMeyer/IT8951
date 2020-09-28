# IT8951

This Python 3 module implements a driver for the IT8951 e-paper controller, via SPI.
The driver was developed using the 6-inch e-Paper HAT from Waveshare. It hopefully will work for
other (related) hardware too.

To install, clone the repository, enter the directory and run
```
pip install -r requirements.txt
pip install ./
```

---

### Examples

To display a bitmap image:

```
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

To display some text:

```
from IT8951.display import AutoEPDDisplay
from IT8951 import constants

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

### Updates for version 0.1.0

For this version the backend was rewritten, so that the SPI communication happens directly
by communicating with the Linux kernel through `/dev/spidev*`. This means:

 - `sudo` no longer required
 - requires neither the `bcm2835` C library nor the `spidev` Python module
 - data transfer is way faster than before!

### Hacking

If you modify `spi.pyx`, make sure to set the `USE_CYTHON` environment variable before building---otherwise your
changes will not be compiled into `spi.c`.
