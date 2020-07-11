import struct
import math


def short_to_degree(value: int) -> float:
    return value / 65535.0 * 360


def degree_to_radian(value: float) -> float:
    return value * (math.pi / 180.0)


def half_float_convert(value: int) -> float:

    # ushort (2 bytes) -> float (4 bytes) | requires signed short as input
    valConv = value
    if value < 0:
        valConv &= 0x00007FFF
        valConv |= 0xFFFC0000
    valConv <<= 0x0D
    valConv += 0x38000000
    valConv &= 0xFFFFFFFF
    return struct.unpack('f', struct.pack('I', valConv))[0]

    # alternative (only python >= 3.6)
    #return struct.unpack('e', struct.pack('H', value))[0]
