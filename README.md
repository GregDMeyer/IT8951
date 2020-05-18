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
clock frequency. In my experience, you can only increase the frequency for the pixel transfer, if you
increase it too much for any other data transfer the transfer will fail.

The SPI frequency for transferring pixel data is currently hardcoded at 24 MHz, which is the maximum
stated in the IT8951 chip spec [here](https://www.waveshare.com/w/upload/1/18/IT8951_D_V0.2.4.3_20170728.pdf)
(page 41). But, you could try setting higher and seeing if it works anyway. It is set on line 208 of `IT8951/spi.pyx`.
If you change `spi.pyx`, don't forget to tell `setup.py` to use Cython when you build or your change won't have
any effect.

### Updates for version 0.1.0

For this version the backend was rewritten, so that the SPI communication happens directly
by communicating with the Linux kernel through `/dev/spidev*`. This means:

 - `sudo` no longer required
 - requires neither the `bcm2835` C library nor the `spidev` Python module
 - data transfer is way faster than before!