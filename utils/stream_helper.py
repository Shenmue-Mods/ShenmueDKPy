import typing
import struct
from utils.math import half_float_convert


def sread_byte(binary_stream: typing.BinaryIO):
    bytes = binary_stream.read(1)
    if len(bytes) != 1:
        return 0
    return struct.unpack('B', bytes)[0]


def sread_ushort(binary_stream: typing.BinaryIO):
    bytes = binary_stream.read(2)
    if len(bytes) != 2:
        return 0
    return struct.unpack('H', bytes)[0]


def sread_short(binary_stream: typing.BinaryIO):
    bytes = binary_stream.read(2)
    if len(bytes) != 2:
        return 0
    return struct.unpack('h', bytes)[0]


def sread_uint(binary_stream: typing.BinaryIO):
    bytes = binary_stream.read(4)
    if len(bytes) != 4:
        return 0
    return struct.unpack('I', bytes)[0]


def sread_int(binary_stream: typing.BinaryIO):
    bytes = binary_stream.read(4)
    if len(bytes) != 4:
        return 0
    return struct.unpack('i', bytes)[0]


def sread_float(binary_stream: typing.BinaryIO):
    bytes = binary_stream.read(4)
    if len(bytes) != 4:
        return 0
    return struct.unpack('f', bytes)[0]


def sread_hfloat(binary_stream: typing.BinaryIO):
    return half_float_convert(sread_short(binary_stream))


def sreadstr(binary_stream: typing.BinaryIO):
    string = str()
    while binary_stream.readable():
        character = int.from_bytes(binary_stream.read(1), byteorder='little')
        if character == 0:
            break
        string = string + chr(character)
    return string
