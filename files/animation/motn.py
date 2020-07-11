#!/usr/bin/python3

import json

from files.file import File
from utils.stream_helper import *
from utils.model import *

#import matplotlib
#import matplotlib.pyplot as plt


def dbg_print(*args, **kwargs):
    print("".join(map(str, args)), **kwargs)


class MOTN(File):
    class Header:
        """ The MOTN header object containing the offsets and attribute flags

            Attributes:
                data_table_offset (int): Offset to the beginning of the sequence data offset table
                name_table_offset (int): Offset to the beginning of the sequence name offset table
                data_offset (int): Offset to the beginning of the sequence data
                attributes (int): Attributes or flags of the file
                file_size (int): Size of the file
        """

        def __init__(self):
            self.data_table_offset = 0
            self.name_table_offset = 0
            self.data_offset = 0
            self.attributes = 0
            self.file_size = 0

        def read(self, binary_stream: typing.BinaryIO):
            self.data_table_offset = sread_uint(binary_stream)
            self.name_table_offset = sread_uint(binary_stream)
            self.data_offset = sread_uint(binary_stream)
            self.attributes = sread_uint(binary_stream)
            self.file_size = sread_uint(binary_stream)

        def write(self, binary_stream: typing.BinaryIO):
            binary_stream.write(self.data_table_offset.to_bytes(4, byteorder='little'))
            binary_stream.write(self.name_table_offset.to_bytes(4, byteorder='little'))
            binary_stream.write(self.data_offset.to_bytes(4, byteorder='little'))
            binary_stream.write(self.attributes.to_bytes(4, byteorder='little'))
            binary_stream.write(self.file_size.to_bytes(4, byteorder='little'))

        def animation_count(self):
            return (self.attributes & 0x0FFF) - 1

        def __str__(self):
            return json.dumps(json.loads('{ "MOTN_Header": { "name_table_offset": ' + str(self.name_table_offset) +
                                         ', "data_table_offset": ' + str(self.data_table_offset) +
                                         ', "data_offset": ' + str(self.data_offset) +
                                         ', "attributes": ' + str(self.attributes) +
                                         ', "file_size": ' + str(self.file_size) + '}}'), indent=4)

    class Sequence:
        """ The MOTN sequence object containing the data of a sequence

            Attributes:
                name (str): Name of the sequence retrieved from the sequence name table
                data_offset (int): Offset to sequence data relative to the file sequence data offset from the header
                extra_data_offset (int): Offset to sequence extra/unknown data relative to the file sequence data offset
                                         from the header
                data (SequenceData): Sequence data object containing the actual sequence data
                extra_data (SequenceExtraData): Sequence extra data object containing the extra/unknown sequence data
        """

        class SequenceExtraData:
            """ The MOTN sequence extra/unknown data object containing the extra/unknown data of a sequence

                Attributes:
                    data (str): Actual data
            """

            def __init__(self):
                self.unknown_data = []
                self.unknown_12_block = 0
                self.more_data = []

                self.unknown_13_value = 0  # + 1 (MOTM + count * 8 + 4 = this)
                self.unknown_14_value = 0  # + 2 (MOTM + count * 8 + 8 = this)
                self.unknown_15_count = 0  # + 3 (MOTM + count * 8)
                self.unknown_16 = 0

                # unknown lut (0xF7 Mask)
                self.count_lut_1 = [
                    0x0C, 0x04, 0x08, 0x10, 0x14, 0x0C, 0x08, 0x04, 0x00, 0x10, 0x08, 0x0C, 0x04, 0x04, 0x10, 0x08,
                    0x02, 0x08, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04, 0x08, 0x08, 0x04, 0x00, 0x00, 0x00,
                ]

                # unknown lut 2 - electric boogaloo
                self.count_lut_2 = [
                    0x00, 0x00, 0x09, 0x11, 0x00, 0x00, 0x0A, 0x11, 0x00, 0x01, 0x02, 0x11, 0x00, 0x01, 0x05, 0x11,
                    0x00, 0x01, 0x08, 0x11, 0x00, 0x01, 0x0B, 0x11, 0x00, 0x01, 0x0F, 0x11, 0x00, 0x01, 0x10, 0x11,
                    0x00, 0x01, 0x11, 0x11, 0x00, 0x01, 0x12, 0x11, 0x00, 0x01, 0x13, 0x11, 0x00, 0x01, 0x14, 0x11,
                    0x00, 0x01, 0x15, 0x11, 0x00, 0x01, 0x16, 0x11, 0x00, 0x01, 0x17, 0x11, 0x00, 0x01, 0x18, 0x11,
                    0x00, 0x01, 0x19, 0x11, 0x01, 0x00, 0x00, 0x00, 0x00, 0x04, 0x04, 0x10, 0x08, 0x08, 0x08, 0x08,
                    0x04, 0x04, 0x10, 0x08, 0x08, 0x04, 0x08, 0x04, 0x04, 0x04, 0x08, 0x08, 0x08, 0x04, 0x08, 0x08,
                    0x08, 0x10, 0x0C, 0x1C, 0x04, 0x08, 0x08, 0x04, 0x08, 0x08, 0x08, 0x08, 0x08, 0x0C, 0x08, 0x0C,
                    0x08, 0x08, 0x04, 0x08, 0x08, 0x04, 0x04, 0x04, 0x04, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
                ]

            def __str__(self):
                return json.dumps(json.loads('{ "SequenceExtraData":'
                                             '{ "unknown_data": ' + str(self.unknown_data) +
                                             ', "more_data": ' + str(self.more_data) +
                                             ', "unknown_12_block": ' + str(self.unknown_12_block) +
                                             ', "unknown_13_value": ' + str(self.unknown_13_value) +
                                             ', "unknown_14_value": ' + str(self.unknown_14_value) +
                                             ', "unknown_15_count": ' + str(self.unknown_15_count) +
                                             ', "unknown_16": ' + str(self.unknown_16) + '}}'), indent=4)

            def calc_count(self, value):
                value = value & 0x1F
                return self.count_lut_1[value]

            def read(self, binary_stream: typing.BinaryIO):
                offset = binary_stream.tell()
                # skip unknown extra data
                return

                # (WIP) Needs waaaaay more research

                if False:
                    # first parser implementation

                    # skip 0x0C (12)
                    for i in range(0, 12, 1):
                        self.unknown_data.append(sread_byte(binary_stream))

                    val = sread_byte(binary_stream)
                    while val != 1 and val > 0:
                        count = self.calc_count(val)
                        self.more_data.append(val)
                        for i in range(0, count - 1, 1):
                            self.more_data.append(sread_byte(binary_stream))
                        val = sread_byte(binary_stream)
                    binary_stream.seek(-1, 1)

                    self.unknown_12_block = sread_byte(binary_stream)
                    self.unknown_13_value = sread_byte(binary_stream)
                    self.unknown_14_value = sread_byte(binary_stream)
                    self.unknown_15_count = sread_byte(binary_stream)
                else:
                    # parser 3 implementation

                    # skip 0x0C (12)
                    for i in range(0, 12, 1):
                        self.unknown_data.append(sread_byte(binary_stream))

                    # 8 is important? 8 checks everywhere
                    # if 8 read next values at + 6 from 8 (ITS A COUNT OF SOMETHING BOI)
                    # it happens in between this whole reading process

                    val = sread_byte(binary_stream)
                    while val != 1 and val > 0:
                        count = self.calc_count(val)
                        self.more_data.append(val)
                        for i in range(0, count - 1, 1):
                            self.more_data.append(sread_byte(binary_stream))
                        val = sread_byte(binary_stream)

                        # magic 8 check
                        if val == 8:
                            break

                    # go back to 8 (just for sanity sake)
                    binary_stream.seek(-1, 1)

                    # skip to the needed value
                    binary_stream.seek(6, 1)
                    self.unknown_12_block = sread_byte(binary_stream)
                    self.unknown_13_value = sread_byte(binary_stream)
                    self.unknown_14_value = sread_byte(binary_stream)
                    self.unknown_15_count = sread_byte(binary_stream)

        class SequenceData:
            """ The MOTN sequence data object containing the actual data of a sequence

                Attributes:
                    header (SequenceDataHeader): Header object of the sequence data
            """

            class SequenceDataHeader:
                """ The MOTN sequence data header object containing the flags and offsets of the sequence data

                    Attributes:
                        frame_count_flags (int): Frame count and flags
                        block_2_offset (int): Offset to the block 2 of sequence data relative to header offset
                        block_3_offset (int): Offset to the block 3 of sequence data relative to header offset
                        block_4_offset (int): Offset to the block 4 of sequence data relative to header offset
                        block_5_offset (int): Offset to the block 5 of sequence data relative to header offset
                """

                def __init__(self):
                    self.frame_count_flags = 0
                    self.block_2_offset = 0
                    self.block_3_offset = 0
                    self.block_4_offset = 0
                    self.block_5_offset = 0

                def __len__(self):
                    return 12

                def read(self, binary_stream: typing.BinaryIO):
                    offset = binary_stream.tell()
                    self.frame_count_flags = sread_uint(binary_stream)
                    self.block_2_offset = sread_ushort(binary_stream)
                    self.block_3_offset = sread_ushort(binary_stream)
                    self.block_4_offset = sread_ushort(binary_stream)
                    self.block_5_offset = sread_ushort(binary_stream)

                def write(self, binary_stream: typing.BinaryIO):
                    binary_stream.write(self.frame_count_flags.to_bytes(4, byteorder='little'))
                    binary_stream.write(self.block_2_offset.to_bytes(2, byteorder='little'))
                    binary_stream.write(self.block_3_offset.to_bytes(2, byteorder='little'))
                    binary_stream.write(self.block_4_offset.to_bytes(2, byteorder='little'))
                    binary_stream.write(self.block_5_offset.to_bytes(2, byteorder='little'))

                def frame_count(self) -> int:
                    return self.frame_count_flags & 0x7FFF

                def block_2_half(self) -> bool:
                    # uses the frame count to check what formatting the data has
                    return (self.frame_count_flags & 0xFFFF8000) >= 0

                def block_3_half(self) -> bool:
                    # uses the frame count to check what formatting the data has
                    return (self.frame_count_flags & 0x7FFF) <= 0xFF

            class SequenceBoneData:
                """ Sequence data for a single bone.

                    Attributes:
                        bone_index (int): Frame count and flags
                        pos_x (list): Position X-Axis keyframes
                        pos_y (list): Position Y-Axis keyframes
                        pos_z (list): Position Z-Axis keyframes
                        rot_x (list): Rotation X-Axis keyframes in radian
                        rot_y (list): Rotation Y-Axis keyframes in radian
                        rot_z (list): Rotation Z-Axis keyframes in radian
                        scl_x (list): Scale X-Axis keyframes
                        scl_y (list): Scale Y-Axis keyframes
                        scl_z (list): Scale Z-Axis keyframes
                """

                def __init__(self, bone_index):
                    self.bone_index = bone_index
                    self.pos_x = []
                    self.pos_y = []
                    self.pos_z = []
                    self.rot_x = []
                    self.rot_y = []
                    self.rot_z = []
                    self.scl_x = []
                    self.scl_y = []
                    self.scl_z = []

            class KeyFrame:
                """ Sequence keyframe

                    Attributes:
                        bone_index (int): Frame count and flags
                        frame (int): Frame index of the keyframe
                        time (float): Timestamp of the keyframe
                        value (float): Position/Radian value of the keyframe
                        linear (list): Linear pair (start slope, end slope)
                """

                def __init__(self, frame, time, bone_index, value=0.0):
                    self.frame = frame
                    self.time = time
                    self.bone_index = bone_index
                    self.value = value
                    self.linear = [0.0, 0.0]
                    self.has_value = False

                def set_value(self, value):
                    self.value = value
                    self.has_value = True

            def __init__(self):
                self.header = self.SequenceDataHeader()

                self.base_offset = 0

                self.bone_index_offset = 0                  # block 1 reading offset, keeps track of position in block.
                self.keyframe_counts_offset = 0             # block 2 reading offset, keeps track of position in block.
                self.keyframe_indices_offset = 0            # block 3 reading offset, keeps track of position in block.
                self.keyframe_block_types_offset = 0        # block 4 reading offset, keeps track of position in block.
                self.float_data_offset = 0                  # block 5 reading offset, keeps track of position in block.

                self.bone_index = 0
                self.seconds_per_frame = 0.033333335

                self.bone_keyframes = []

                self.keyframe_block_size_lut = [0, 1, 2, 3, 1, 2, 3, 4, 2, 3, 4, 5, 3, 4, 5, 6,
                                                1, 2, 3, 4, 2, 3, 4, 5, 3, 4, 5, 6, 4, 5, 6, 7,
                                                2, 3, 4, 5, 3, 4, 5, 6, 4, 5, 6, 7, 5, 6, 7, 8,
                                                3, 4, 5, 6, 4, 5, 6, 7, 5, 6, 7, 8, 6, 7, 8, 9,
                                                1, 2, 3, 4, 2, 3, 4, 5, 3, 4, 5, 6, 4, 5, 6, 7,
                                                2, 3, 4, 5, 3, 4, 5, 6, 4, 5, 6, 7, 5, 6, 7, 8,
                                                3, 4, 5, 6, 4, 5, 6, 7, 5, 6, 7, 8, 6, 7, 8, 9,
                                                4, 5, 6, 7, 5, 6, 7, 8, 6, 7, 8, 9, 7, 8, 9, 10,
                                                2, 3, 4, 5, 3, 4, 5, 6, 4, 5, 6, 7, 5, 6, 7, 8,
                                                3, 4, 5, 6, 4, 5, 6, 7, 5, 6, 7, 8, 6, 7, 8, 9,
                                                4, 5, 6, 7, 5, 6, 7, 8, 6, 7, 8, 9, 7, 8, 9, 10,
                                                5, 6, 7, 8, 6, 7, 8, 9, 7, 8, 9, 10, 8, 9, 10, 11,
                                                3, 4, 5, 6, 4, 5, 6, 7, 5, 6, 7, 8, 6, 7, 8, 9,
                                                4, 5, 6, 7, 5, 6, 7, 8, 6, 7, 8, 9, 7, 8, 9, 10,
                                                5, 6, 7, 8, 6, 7, 8, 9, 7, 8, 9, 10, 8, 9, 10, 11,
                                                6, 7, 8, 9, 7, 8, 9, 10, 8, 9, 10, 11, 9, 10, 11, 12]

            def read(self, binary_stream: typing.BinaryIO):
                self.base_offset = binary_stream.tell()
                self.header.read(binary_stream)
                self.bone_index_offset = binary_stream.tell()
                self.keyframe_counts_offset = self.base_offset + self.header.block_2_offset
                self.keyframe_indices_offset = self.base_offset + self.header.block_3_offset
                self.keyframe_block_types_offset = self.base_offset + self.header.block_4_offset
                self.float_data_offset = self.base_offset + self.header.block_5_offset

                self.bone_index = 0
                instruction = sread_ushort(binary_stream)
                self.bone_index_offset = binary_stream.tell()
                while self.bone_index < 127:
                    if instruction == 0:
                        break

                    if self.bone_index == (instruction >> 9):
                        bone_data = self.SequenceBoneData(self.bone_index)

                        if instruction & 0x1C0:
                            if instruction & 0x100:
                                # PosX
                                bone_data.pos_x = self.read_keyframes(binary_stream)
                            if instruction & 0x80:
                                # PosY
                                bone_data.pos_y = self.read_keyframes(binary_stream)
                            if instruction & 0x40:
                                # PosZ
                                bone_data.pos_z = self.read_keyframes(binary_stream)
                        if instruction & 0x38:
                            if instruction & 0x20:
                                # RotX
                                bone_data.rot_x = self.read_keyframes(binary_stream)
                            if instruction & 0x10:
                                # RotY
                                bone_data.rot_y = self.read_keyframes(binary_stream)
                            if instruction & 0x08:
                                # RotZ
                                bone_data.rot_z = self.read_keyframes(binary_stream)
                        if instruction & 0x07:  # seems to be unused in shenmue atm
                            if instruction & 0x04:
                                # SclX
                                bone_data.scl_x = self.read_keyframes(binary_stream)
                            if instruction & 0x02:
                                # SclY
                                bone_data.scl_y = self.read_keyframes(binary_stream)
                            if instruction & 0x01:
                                # SclZ
                                bone_data.scl_z = self.read_keyframes(binary_stream)

                        binary_stream.seek(self.bone_index_offset)
                        instruction = sread_ushort(binary_stream)
                        self.bone_index_offset = binary_stream.tell()
                        self.bone_keyframes.append(bone_data)

                        # animation per bone plot
                        #x = []
                        #y = []
                        #for keyframe in bone_data.pos_x:
                        #    x.append(keyframe.frame)
                        #    y.append(keyframe.value)
                        #fig, ax = plt.subplots()
                        #ax.plot(x, y, label='pos_x', marker='o')
                        #ax.set(ylabel='value', xlabel='frame', title='motion data (' + str(IKBoneID(self.bone_index)) + ')')
                        #ax.grid()
                        #x.clear()
                        #y.clear()

                        #for keyframe in bone_data.pos_y:
                        #    x.append(keyframe.frame)
                        #    y.append(keyframe.value)
                        #ax.plot(x, y, label='pos_y', marker='o')
                        #x.clear()
                        #y.clear()

                        #for keyframe in bone_data.pos_z:
                        #    x.append(keyframe.frame)
                        #    y.append(keyframe.value)
                        #ax.plot(x, y, label='pos_z', marker='o')
                        #x.clear()
                        #y.clear()

                        #for keyframe in bone_data.rot_x:
                        #    x.append(keyframe.frame)
                        #    y.append(keyframe.value)
                        #ax.plot(x, y, label='rot_x', marker='o')
                        #x.clear()
                        #y.clear()

                        #for keyframe in bone_data.rot_y:
                        #    x.append(keyframe.frame)
                        #    y.append(keyframe.value)
                        #ax.plot(x, y, label='rot_y', marker='o')
                        #x.clear()
                        #y.clear()

                        #for keyframe in bone_data.rot_z:
                        #    x.append(keyframe.frame)
                        #    y.append(keyframe.value)
                        #ax.plot(x, y, label='rot_z', marker='o')
                        #x.clear()
                        #y.clear()

                        #plt.legend(loc="upper right")
                        #plt.show()

                    self.bone_index += 1

            def read_keyframes(self, binary_stream: typing.BinaryIO):

                keyframes = []

                # read block 2 value (sizes)
                keyframe_count = 0
                binary_stream.seek(self.keyframe_counts_offset)
                if self.header.block_2_half():
                    keyframe_count = sread_byte(binary_stream)
                else:
                    keyframe_count = sread_ushort(binary_stream)
                self.keyframe_counts_offset = binary_stream.tell()

                # add initial keyframe time/frame
                keyframe_frames = [0]

                # read keyframe times/frames
                binary_stream.seek(self.keyframe_indices_offset)
                if self.header.block_3_half():
                    for i in range(0, keyframe_count, 1):
                        keyframe_frame = sread_byte(binary_stream)
                        keyframe_frames.append(keyframe_frame)
                else:
                    for i in range(0, keyframe_count, 1):
                        keyframe_frame = sread_ushort(binary_stream)
                        keyframe_frames.append(keyframe_frame)
                self.keyframe_indices_offset = binary_stream.tell()

                # add last keyframe time/frame
                keyframe_frames.append(self.header.frame_count())

                # add two keyframes which are always implied and needed
                keyframe_count = keyframe_count + 2

                # divide by 4 to create the keyframe block count
                keyframe_block_count = keyframe_count >> 2

                # keyframe count of 3 are added up to make a whole 4 keyframe block
                if keyframe_count & 3:
                    keyframe_block_count += 1

                # if no keyframe blocks exist skip.
                if not keyframe_block_count:
                    return

                # pre calc block 5 size for comparison only
                block_5_count = 0
                first_count_tmp = keyframe_block_count
                block_4_offset_tmp = self.keyframe_block_types_offset
                while first_count_tmp:
                    binary_stream.seek(block_4_offset_tmp)
                    keyframe_block_type = sread_byte(binary_stream)
                    block_4_offset_tmp += 1
                    block_5_count += 2 * self.calc_keyframe_block_size(keyframe_block_type)
                    first_count_tmp -= 1

                binary_stream.seek(self.float_data_offset)
                before_offset = binary_stream.tell()

                last_keyframe_value = 0.0
                keyframe_index = 0

                while keyframe_block_count:

                    binary_stream.seek(self.keyframe_block_types_offset)
                    keyframe_block_type = sread_byte(binary_stream)
                    keyframe_block_size = self.calc_keyframe_block_size(keyframe_block_type)

                    binary_stream.seek(self.float_data_offset)

                    if keyframe_block_type & 0xFF:

                        # keyframe 1 of block
                        if keyframe_block_type & 0xC0:
                            frame = keyframe_frames[keyframe_index]
                            keyframe = self.KeyFrame(frame, frame * self.seconds_per_frame,
                                                     self.bone_index, last_keyframe_value)
                            keyframe_index += 1

                            if keyframe_block_type & 0x80:
                                val = sread_hfloat(binary_stream)
                                keyframe.linear[0] = val
                                val = sread_hfloat(binary_stream)
                                keyframe.linear[1] = val

                            if keyframe_block_type & 0x40:
                                val = sread_hfloat(binary_stream)
                                last_keyframe_value = val
                                keyframe.set_value(val)

                            keyframes.append(keyframe)

                        # keyframe 2 of block
                        if keyframe_block_type & 0x30:
                            frame = keyframe_frames[keyframe_index]
                            keyframe = self.KeyFrame(frame, frame * self.seconds_per_frame,
                                                     self.bone_index, last_keyframe_value)
                            keyframe_index += 1

                            if keyframe_block_type & 0x20:
                                val = sread_hfloat(binary_stream)
                                keyframe.linear[0] = val
                                val = sread_hfloat(binary_stream)
                                keyframe.linear[1] = val

                            if keyframe_block_type & 0x10:
                                val = sread_hfloat(binary_stream)
                                last_keyframe_value = val
                                keyframe.set_value(val)

                            keyframes.append(keyframe)

                        # keyframe 3 of block
                        if keyframe_block_type & 0x0C:
                            frame = keyframe_frames[keyframe_index]
                            keyframe = self.KeyFrame(frame, frame * self.seconds_per_frame,
                                                     self.bone_index, last_keyframe_value)
                            keyframe_index += 1

                            if keyframe_block_type & 0x08:
                                val = sread_hfloat(binary_stream)
                                keyframe.linear[0] = val
                                val = sread_hfloat(binary_stream)
                                keyframe.linear[1] = val

                            if keyframe_block_type & 0x04:
                                val = sread_hfloat(binary_stream)
                                last_keyframe_value = val
                                keyframe.set_value(val)

                            keyframes.append(keyframe)

                        # keyframe 4 of block
                        if keyframe_block_type & 0x03:
                            frame = keyframe_frames[keyframe_index]
                            keyframe = self.KeyFrame(frame, frame * self.seconds_per_frame,
                                                     self.bone_index, last_keyframe_value)
                            keyframe_index += 1

                            if keyframe_block_type & 0x02:
                                val = sread_hfloat(binary_stream)
                                keyframe.linear[0] = val
                                val = sread_hfloat(binary_stream)
                                keyframe.linear[1] = val

                            if keyframe_block_type & 0x01:
                                val = sread_hfloat(binary_stream)
                                last_keyframe_value = val
                                keyframe.set_value(val)

                            keyframes.append(keyframe)

                    new_block_5_offset = binary_stream.tell()
                    self.float_data_offset += 2 * keyframe_block_size

                    # check for misaligned block 5 reading if we encounter new type of animations
                    if self.float_data_offset != new_block_5_offset:
                        print('Misaligned Block 5 Offset! ', new_block_5_offset - self.float_data_offset)

                    keyframe_block_count -= 1
                    self.keyframe_block_types_offset += 1

                new_block_5_offset = binary_stream.tell()
                new_size = new_block_5_offset - before_offset
                if new_size != block_5_count:
                    print('Wrong Block 5 Size! ', new_size, ' != ', block_5_count)

                # check for last keyframe existence and add if non existing
                if len(keyframes):
                    last_keyframe = keyframes[-1]
                    if last_keyframe.frame is not keyframe_frames[-1]:
                        frame = keyframe_frames[-1]
                        keyframe = self.KeyFrame(frame, frame * self.seconds_per_frame,
                                                 self.bone_index, last_keyframe_value)
                        keyframes.append(keyframe)

                return keyframes

            def calc_keyframe_block_size(self, value):
                result = 0
                result += 2 if (value & 0x80) else 0
                result += 1 if (value & 0x40) else 0
                result += 2 if (value & 0x20) else 0
                result += 1 if (value & 0x10) else 0
                result += 2 if (value & 0x08) else 0
                result += 1 if (value & 0x04) else 0
                result += 2 if (value & 0x02) else 0
                result += 1 if (value & 0x01) else 0
                return result

        def __init__(self):
            self.name = 'NO_NAME'
            self.data_offset = 0
            self.extra_data_offset = 0
            self.data = self.SequenceData()
            self.extra_data = self.SequenceExtraData()

    def __init__(self):
        super().__init__()
        self.header = self.Header()
        self.sequences = []

    def _read(self, binary_stream):
        self.header.read(binary_stream)

        # read sequence names
        offset = 0
        binary_stream.seek(self.base_offset + self.header.name_table_offset)
        for i in range(0, self.header.animation_count(), 1):
            sequence = self.Sequence()
            string_offset = sread_uint(binary_stream)
            offset = binary_stream.tell()
            binary_stream.seek(self.base_offset + string_offset)
            sequence.name = sreadstr(binary_stream)
            self.sequences.append(sequence)
            binary_stream.seek(self.base_offset + offset)

        # read sequence offsets
        binary_stream.seek(self.base_offset + self.header.data_table_offset)
        for sequence in self.sequences:
            sequence.data_offset = sread_uint(binary_stream)
            sequence.extra_data_offset = sread_int(binary_stream)

        extra_data_dict = {}
        data_dict = {}

        # read sequence data
        for sequence in self.sequences:

            # read extra data
            extra_data_offset = self.base_offset + sequence.extra_data_offset
            binary_stream.seek(extra_data_offset)
            sequence.extra_data.read(binary_stream)

            # debug offset dict
            if extra_data_offset in extra_data_dict:
                extra_data_dict[extra_data_offset] += 1
            else:
                extra_data_dict[extra_data_offset] = 1

            # read data
            data_offset = self.base_offset + self.header.data_offset + sequence.data_offset

            # data offset dict
            if data_offset in data_dict:
                data_dict[data_offset] += 1
            else:
                data_dict[data_offset] = 1

            # debug selection
            # 956058 = Walk
            if (data_offset != 956058):
                continue

            #print(sequence.name)
            #print(data_offset)
            #print(extra_data_offset)

            binary_stream.seek(data_offset)
            sequence.data.read(binary_stream)

        # a lot of extra data crap (kinda useless for exporting animations)
        #extra_data_offsets = list(sorted(extra_data_dict.keys()))
        #extra_data_val_dict = {}
        #for i in range(0, len(extra_data_offsets) - 1, 1):
        #    offset = extra_data_offsets[i]
        #    binary_stream.seek(offset)
        #    size = extra_data_offsets[i + 1] - offset
        #    if size in extra_data_val_dict:
        #        extra_data_val_dict[size].append(offset)
        #    else:
        #        extra_data_val_dict[size] = [offset]
        #print(extra_data_val_dict)

        return True

    def _write(self, binary_stream):
        return True

    def _clean(self):
        return True
