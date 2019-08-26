# IT8951

This Python module implements a driver for the IT8951 e-paper controller, via SPI. 
The driver was developed using the 6-inch e-Paper HAT from Waveshare. It hopefully will work for 
other (related) hardware too.

Building the driver requires first installing the bcm2835 C library, which can be found 
[here](http://www.airspayce.com/mikem/bcm2835/) if you don't already have it.

Once you have that installed, clone the repository, enter the directory and run
```
pip install requirements.txt
pip install ./
```

---

For some examples of usage, take a look at the integration tests.
