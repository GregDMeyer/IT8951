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
