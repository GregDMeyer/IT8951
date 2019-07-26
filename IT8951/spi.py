
import numpy as np
import os
import ctypes

module_dir = os.path.dirname(os.path.abspath(__file__))
so = ctypes.CDLL(os.path.join(module_dir, 'IT8951.so'))

class SPI:

    def __init__(self):
        so.IT8951_Init()

    def __del__(self):
        so.IT8951_Cancel()

    def read(self, preamble, count):
        buf = (ctypes.c_ushort*count)()
        so.Read(preamble, count, buf)
        return buf

    def write(self, preamble, ary):
        buf = np.ascontiguousarray(ary, dtype=np.uint16)
        buf_p = buf.ctypes.data_as(c_ushort)
        return so.Write(preamble, len(vals), buf_p)
