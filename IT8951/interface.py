
from . import constants
from .constants import Pins, Commands, Registers, DisplayModes, PixelModes
from .spi import SPI

from time import sleep

import RPi.GPIO as GPIO
import numpy as np

class EPD:
    '''
    An interface to the electronic paper display (EPD).

    Parameters
    ----------

    vcom : float
         The VCOM voltage that produces optimal contrast. Varies from
         device to device.
    '''

    def __init__(self, vcom=-1.5):

        # bus 0, device 0
        self.spi = SPI()

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        # GPIO.setup(Pins.CS, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(Pins.HRDY, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(Pins.RESET, GPIO.OUT, initial=GPIO.HIGH)

        # reset
        GPIO.output(Pins.RESET, GPIO.LOW)
        sleep(0.1)
        GPIO.output(Pins.RESET, GPIO.HIGH)

        self.width  = None
        self.height = None
        self.img_buf_address  = None
        self.firmware_version = None
        self.lut_version      = None
        self.update_system_info()

        # TODO: should send INIT command?

        # enable I80 packed mode
        self.write_register(Registers.I80CPCR, 0x1)

        self.set_vcom(vcom)

    def __del__(self):
        GPIO.cleanup()

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
        # print('sending command {:x} with data {}'.format(cmd, str(args)))
        #GPIO.output(Pins.CS, GPIO.LOW)
        self.spi.write(0x6000, [cmd])  # 0x6000 is preamble
        #GPIO.output(Pins.CS, GPIO.HIGH)

        for arg in args:
            # print('arg:', arg)
            self.write_data(arg)

    def write_data(self, ary):
        '''
        Send the device an array of data

        Parameters
        ----------

        ary : array-like
            The data
        '''
        # GPIO.output(Pins.CS, GPIO.LOW)
        self.spi.write(0x0000, ary)
        # GPIO.output(Pins.CS, GPIO.HIGH)

    def read_data(self, n):
        '''
        Read n 16-bit words of data from the device

        Parameters
        ----------

        n : int
            The number of 2-byte words to read
        '''
        # TODO: add buf as argument?
        # GPIO.output(Pins.CS, GPIO.LOW)
        rtn = self.spi.read(0x1000, n)
        # GPIO.output(Pins.CS, GPIO.HIGH)
        return rtn

    def read_int(self):
        '''
        Read a single 16 bit int from the device
        '''
        recv = self.read_data(1)[0]
        return recv

    def run(self):
        self.write_cmd(Commands.SYS_RUN)

    def standby(self):
        self.write_cmd(Commands.STANDBY)

    def sleep(self):
        self.write_cmd(Commands.SLEEP)

    def read_register(self, address):
        self.write_cmd(Commands.REG_RD, address)
        return self.read_int()

    def write_register(self, address, val):
        self.write_cmd(Commands.REG_WR, address)
        self.write_data((val,))

    def mem_burst_read_trigger(self, address, count):
        # these are both 32 bits, so we need to split them
        # up into two 16 bit values

        addr0 = address & 0xFFFF
        addr1 = address >> 16

        len0 = count & 0xFFFF
        len1 = count >> 16

        self.write_cmd(Commands.MEM_BST_RD_T,
                       addr0, addr1, len0, len1)

    def mem_burst_read_start(self):
        self.write_cmd(Commands.MEM_BST_RD_S)

    def mem_burst_write(self, address, count):
        addr0 = address & 0xFFFF
        addr1 = address >> 16

        len0 = count & 0xFFFF
        len1 = count >> 16

        self.write_cmd(Commands.MEM_BST_WR,
                       addr0, addr1, len0, len1)

    def mem_burst_end(self):
        self.write_cmd(Commands.MEM_BST_END)

    def get_vcom(self):
        self.write_cmd(Commands.VCOM, 0)
        vcom_int = self.read_int()
        return -vcom_int/1000

    def set_vcom(self, vcom):
        self._validate_vcom(vcom)
        vcom_int = int(-1000*vcom)
        self.write_cmd(Commands.VCOM, 1, vcom_int)

    def _validate_vcom(self, vcom):
        # TODO: figure out the actual limits for vcom
        if not -5 < vcom < 0:
            raise ValueError("vcom must be between -5 and 0")

    def update_system_info(self):
        self.write_cmd(Commands.GET_DEV_INFO)
        data = self.read_data(20)
        self.width  = data[0]
        self.height = data[1]
        self.img_buf_address = data[3] << 16 | data[2]
        self.firmware_version = ''.join([chr(x>>8)+chr(x&0xFF) for x in data[4:12]])
        self.lut_version      = ''.join([chr(x>>8)+chr(x&0xFF) for x in data[12:20]])

    def set_img_buf_base_addr(self, address):
        word0 = address >> 16
        word1 = address & 0xFFFF
        self.write_register(Registers.LISAR+2, word0)
        self.write_register(Registers.LISAR, word1)

    def wait_display_ready(self):
        while(self.read_register(Registers.LUTAFSR)):
            sleep(0.01)

    def load_img_start(self, endian_type, pixel_format, rotate_mode):
        arg = (endian_type << 8) | (pixel_format << 4) | rotate_mode
        self.write_cmd(Commands.LD_IMG, arg)

    def load_img_area_start(self, endian_type, pixel_format, rotate_mode, xy, dims):
        arg0 = (endian_type << 8) | (pixel_format << 4) | rotate_mode
        self.write_cmd(Commands.LD_IMG_AREA, arg0, xy[0], xy[1], dims[0], dims[1])

    def load_img_end(self):
        self.write_cmd(Commands.LD_IMG_END)

    def packed_pixel_write(self, buf, rotate_mode=constants.Rotate.NONE, xy=None, dims=None):
        endian_type = constants.EndianTypes.LITTLE
        pixel_format = constants.PixelModes.M_4BPP

        self.set_img_buf_base_addr(self.img_buf_address)
        if xy is None:
            self.load_img_start(endian_type, pixel_format, rotate_mode)
        else:
            self.load_img_area_start(endian_type, pixel_format, rotate_mode, xy, dims)

        buf = self._pack_pixels(buf, pixel_format)
        self.spi.write_pixels(buf)

        self.load_img_end()

    @staticmethod
    def _pack_pixels(buf, pixel_format):
        '''
        Take a buffer where each byte represents a pixel, and pack it
        into 16-bit words according to pixel_format.
        '''
        buf = np.array(buf, dtype=np.ubyte)

        if pixel_format == PixelModes.M_8BPP:
            rtn = np.zeros((buf.size//2,), dtype=np.uint16)
            rtn |= buf[1::2]
            rtn <<= 8
            rtn |= buf[::2]

        elif pixel_format == PixelModes.M_2BPP:
            rtn = np.zeros((buf.size//8,), dtype=np.uint16)
            for i in range(7, -1, -1):
                rtn <<= 2
                rtn |= buf[i::8] >> 6

        elif pixel_format == PixelModes.M_3BPP:
            rtn = np.zeros((buf.size//4,), dtype=np.uint16)
            for i in range(3, -1, -1):
                rtn <<= 4
                rtn |= (buf[i::4] & 0xFE) >> 4

        elif pixel_format == PixelModes.M_4BPP:
            rtn = np.zeros((buf.size//4,), dtype=np.uint16)
            for i in range(3, -1, -1):
                rtn <<= 4
                rtn |= buf[i::4] >> 4

        return rtn

    def display_area(self, xy, dims, display_mode):
        self.write_cmd(Commands.DPY_AREA, xy[0], xy[1], dims[0], dims[1], display_mode)

    def display_area_1bpp(self, xy, dims, display_mode, background_gray, foreground_gray):

        # set display to 1bpp mode
        old_value = self.read_register(Registers.UP1SR+2)
        self.write_register(Registers.UP1SR+2, old_val | (1<<2))

        # set color table
        self.write_register(Registers.BGVR, (background_gray << 8) | foreground_gray)

        # display image
        self.display_area(xy, dims, display_mode)
        self.wait_display_ready()

        # back to normal mode
        old_value = self.read_register(Registers.UP1SR+2)
        self.write_register(Registers.UP1SR+2, old_value & ~(1<<2))

    def display_area_buf(self, xy, dims, display_mode, display_buf_address):
        self.write_cmd(Commands.DPY_BUF_AREA, xy[0], xy[1], dims[0], dims[1], display_mode,
                       display_buf_address & 0xFFFF, display_buf_address >> 16)
