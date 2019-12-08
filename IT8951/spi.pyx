# cython: language_level=3
# cython: profile=True

from cpython cimport array
import array
import time

cdef extern from "bcm2835.h":
     int bcm2835_init()
     int bcm2835_close()

     void bcm2835_gpio_fsel(int, int)
     void bcm2835_gpio_write(int, int)
     void bcm2835_gpio_set_pud(int, int)
     int bcm2835_gpio_lev(int)
     cdef int BCM2835_GPIO_FSEL_OUTP
     cdef int BCM2835_GPIO_FSEL_INPT
     cdef int BCM2835_GPIO_PUD_DOWN
     cdef int LOW
     cdef int HIGH

     int bcm2835_spi_begin()
     void bcm2835_spi_setBitOrder(int)
     void bcm2835_spi_setDataMode(int)
     void bcm2835_spi_setClockDivider(int)
     int bcm2835_spi_transfer(int)
     void bcm2835_spi_end()
     cdef int BCM2835_SPI_BIT_ORDER_MSBFIRST
     cdef int BCM2835_SPI_MODE0
     cdef int BCM2835_SPI_CLOCK_DIVIDER_32

class SPI:

    # TODO move the pin numbers to a default member of the constructor
    # Reference them from there instead of the contsts
    # Remove them from constants.py as well
    def __init__(
        self,
        pin_hrdy=24,
        pin_cs=8,
        pin_reset=17,
    ):
        init_rtn = bcm2835_init()
        if init_rtn != 1:
            raise RuntimeError("Error in bcm2835_init")

        self.pin_hrdy = pin_hrdy
        self.pin_cs = pin_cs
        self.pin_reset = pin_reset

        bcm2835_spi_begin();
        bcm2835_spi_setBitOrder(BCM2835_SPI_BIT_ORDER_MSBFIRST)
        bcm2835_spi_setDataMode(BCM2835_SPI_MODE0)
        bcm2835_spi_setClockDivider(BCM2835_SPI_CLOCK_DIVIDER_32)

        if self.pin_cs is not None:
            bcm2835_gpio_fsel(self.pin_cs, BCM2835_GPIO_FSEL_OUTP);

        if self.pin_reset is not None:
            bcm2835_gpio_fsel(self.pin_reset, BCM2835_GPIO_FSEL_OUTP);

        if self.pin_hrdy is not None:
            bcm2835_gpio_fsel(self.pin_hrdy, BCM2835_GPIO_FSEL_INPT);
            bcm2835_gpio_set_pud(self.pin_hrdy, BCM2835_GPIO_PUD_DOWN);

        self._write_cs(False);

    def __del__(self):
        bcm2835_spi_end()
        bcm2835_close()

    def reset(self):
        assert self.pin_reset is not None
        bcm2835_gpio_write(self.pin_reset, LOW)
        time.sleep(0.1)
        bcm2835_gpio_write(self.pin_reset, HIGH)

    def _write_cs(self, should_listen):
        '''
        Signal the SPI it should listen / not listen.
        Done via self.pin_cs here
        '''
        assert self.pin_cs is not None
        value_to_write = LOW if should_listen else HIGH
        bcm2835_gpio_write(self.pin_cs, value_to_write)

    def wait_ready(self):
        '''
        Wait for the device's ready pin to be set
        '''
        # TODO: should we sleep just a tiny bit here?
        assert self.pin_hrdy is not None
        while not bcm2835_gpio_lev(self.pin_hrdy):
            pass

    def read(self, preamble, count):
        '''
        Send preamble, and return a buffer of 16-bit unsigned ints of length count
        containing the data received
        '''

        # allocate the array we will return
        # initializing it is unnecessary here, but read() is not called
        # with large arrays so this should not be a performance problem
        cdef array.array rtn = array.array('H', (0,)*count)
        cdef unsigned short[:] crtn = rtn

        self.wait_ready()

        self._write_cs(True)

        bcm2835_spi_transfer(preamble>>8)
        bcm2835_spi_transfer(preamble)

        self.wait_ready()

        # spec says to read two dummy bytes
        bcm2835_spi_transfer(0)
        bcm2835_spi_transfer(0)

        self.wait_ready()

        cdef int i
        for i in range(count):
            crtn[i] = bcm2835_spi_transfer(0x00)<<8
            crtn[i] |= bcm2835_spi_transfer(0x00)

        self._write_cs(False)

        return rtn

    def write(self, preamble, ary):
        '''
        Send preamble, and then write the data in ary (16-bit unsigned ints) over SPI
        '''
        cdef array.array buf = array.array('H', ary)
        cdef unsigned short[:] cbuf = buf

        self.wait_ready()

        self._write_cs(True)

        bcm2835_spi_transfer(preamble>>8)
        bcm2835_spi_transfer(preamble)

        self.wait_ready()

        # TODO: what's the best way to do this in cython?
        for i in range(len(ary)):
            bcm2835_spi_transfer(buf[i]>>8)
            bcm2835_spi_transfer(buf[i])

        self._write_cs(False)

    def write_pixels(self, pixbuf):
        '''
        Write the pixels in pixbuf to the device. Pixbuf should be an array of
	16-bit ints, containing packed pixel information.
        '''
        # cdef array.array buf = array.array('H', pixbuf)
        cdef unsigned short[:] cbuf = pixbuf

        cdef unsigned short preamble = 0x0000

        cdef int i
        for i in range(len(cbuf)):
            self.wait_ready()

            self._write_cs(True)

            bcm2835_spi_transfer(preamble>>8)
            bcm2835_spi_transfer(preamble)

            self.wait_ready()

            bcm2835_spi_transfer(cbuf[i] >> 8)
            bcm2835_spi_transfer(cbuf[i])

            self._write_cs(False)

    # the following functions are higher-level for writing and reading
    # various types of data to and from the device

    def write_cmd(self, cmd, *args):
        '''
        Send the device a command code

        Parameters
        ----------

        cmd : int (from constants.Commands)
            The command to send

        args : list(int), optional
            Arguments for the command
        '''
        self.write(0x6000, [cmd])  # 0x6000 is preamble
        for arg in args:
            self.write_data([arg])

    def write_data(self, ary):
        '''
        Send the device an array of data

        Parameters
        ----------

        ary : array-like
            The data
        '''
        self.write(0x0000, ary)

    def read_data(self, n):
        '''
        Read n 16-bit words of data from the device

        Parameters
        ----------

        n : int
            The number of 2-byte words to read
        '''
        return self.read(0x1000, n)

    def read_int(self):
        '''
        Read a single 16 bit int from the device
        '''
        return self.read_data(1)[0]
