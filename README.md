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

For some examples of usage, take a look at the integration tests.

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

#### Running the code on Linux desktop

You can run this library on desktop Linux distributions (e.g. on Ubuntu) to test out things and for faster development. Its is accomplished by opening a `TKInter` window instead of sending the image data to your Pi connected display, on details how to do it check out https://github.com/GregDMeyer/IT8951/blob/master/test/integration/test.py

Windows is curently not supported (the `cython` build will fail because the C code depends on some Linux components). It might work if you use some Linux compatibility layer like `WSL` or `Mingw`.

So to get it working first install `pillow` with `pip`. Do not install `RPi.GPIO` (it is only for the Pi, on desktop it will just exit with an error).

Then install some dependencies:

```
sudo apt-get install python3-dev
sudo apt-get install python3-tk
```

finally compile the cython code:

```
python setup.py build_ext --inplace
```

Now you can run the tests with the `-v` flag: `python test.py -v`.

