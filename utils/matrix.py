import math
import copy
from utils.vector import Vector3, Vector4


class Matrix4(object):

    def __init__(self, row0=Vector4(), row1=Vector4(), row2=Vector4(), row3=Vector4()):
        self.row0 = row0
        self.row1 = row1
        self.row2 = row2
        self.row3 = row3

    def __str__(self):
        return str(self.row0) + '\n' + str(self.row1) + '\n' + str(self.row2) + '\n' + str(self.row3)

    def __getitem__(self, key):
        if key == 0:
            return self.row0.x
        if key == 1:
            return self.row0.y
        if key == 2:
            return self.row0.z
        if key == 3:
            return self.row0.w
        if key == 4:
            return self.row1.x
        if key == 5:
            return self.row1.y
        if key == 6:
            return self.row1.z
        if key == 7:
            return self.row1.w
        if key == 8:
            return self.row2.x
        if key == 9:
            return self.row2.y
        if key == 10:
            return self.row2.z
        if key == 11:
            return self.row2.w
        if key == 12:
            return self.row3.x
        if key == 13:
            return self.row3.y
        if key == 14:
            return self.row3.z
        if key == 15:
            return self.row3.w
        raise IndexError()

    def __setitem__(self, key, value):
        if key == 0:
            self.row0.x = value
        if key == 1:
            self.row0.y = value
        if key == 2:
            self.row0.z = value
        if key == 3:
            self.row0.w = value
        if key == 4:
            self.row1.x = value
        if key == 5:
            self.row1.y = value
        if key == 6:
            self.row1.z = value
        if key == 7:
            self.row1.w = value
        if key == 8:
            self.row2.x = value
        if key == 9:
            self.row2.y = value
        if key == 10:
            self.row2.z = value
        if key == 11:
            self.row2.w = value
        if key == 12:
            self.row3.x = value
        if key == 13:
            self.row3.y = value
        if key == 14:
            self.row3.z = value
        if key == 15:
            self.row3.w = value
        raise IndexError()

    def __mul__(self, other):
        lM11 = self.row0.x
        lM12 = self.row0.y
        lM13 = self.row0.z
        lM14 = self.row0.w
        lM21 = self.row1.x
        lM22 = self.row1.y
        lM23 = self.row1.z
        lM24 = self.row1.w
        lM31 = self.row2.x
        lM32 = self.row2.y
        lM33 = self.row2.z
        lM34 = self.row2.w
        lM41 = self.row3.x
        lM42 = self.row3.y
        lM43 = self.row3.z
        lM44 = self.row3.w

        rM11 = other.row0.x
        rM12 = other.row0.y
        rM13 = other.row0.z
        rM14 = other.row0.w
        rM21 = other.row1.x
        rM22 = other.row1.y
        rM23 = other.row1.z
        rM24 = other.row1.w
        rM31 = other.row2.x
        rM32 = other.row2.y
        rM33 = other.row2.z
        rM34 = other.row2.w
        rM41 = other.row3.x
        rM42 = other.row3.y
        rM43 = other.row3.z
        rM44 = other.row3.w

        m = Matrix4()
        m.row0.x = (((lM11 * rM11) + (lM12 * rM21)) + (lM13 * rM31)) + (lM14 * rM41)
        m.row0.y = (((lM11 * rM12) + (lM12 * rM22)) + (lM13 * rM32)) + (lM14 * rM42)
        m.row0.z = (((lM11 * rM13) + (lM12 * rM23)) + (lM13 * rM33)) + (lM14 * rM43)
        m.row0.w = (((lM11 * rM14) + (lM12 * rM24)) + (lM13 * rM34)) + (lM14 * rM44)
        m.row1.x = (((lM21 * rM11) + (lM22 * rM21)) + (lM23 * rM31)) + (lM24 * rM41)
        m.row1.y = (((lM21 * rM12) + (lM22 * rM22)) + (lM23 * rM32)) + (lM24 * rM42)
        m.row1.z = (((lM21 * rM13) + (lM22 * rM23)) + (lM23 * rM33)) + (lM24 * rM43)
        m.row1.w = (((lM21 * rM14) + (lM22 * rM24)) + (lM23 * rM34)) + (lM24 * rM44)
        m.row2.x = (((lM31 * rM11) + (lM32 * rM21)) + (lM33 * rM31)) + (lM34 * rM41)
        m.row2.y = (((lM31 * rM12) + (lM32 * rM22)) + (lM33 * rM32)) + (lM34 * rM42)
        m.row2.z = (((lM31 * rM13) + (lM32 * rM23)) + (lM33 * rM33)) + (lM34 * rM43)
        m.row2.w = (((lM31 * rM14) + (lM32 * rM24)) + (lM33 * rM34)) + (lM34 * rM44)
        m.row3.x = (((lM41 * rM11) + (lM42 * rM21)) + (lM43 * rM31)) + (lM44 * rM41)
        m.row3.y = (((lM41 * rM12) + (lM42 * rM22)) + (lM43 * rM32)) + (lM44 * rM42)
        m.row3.z = (((lM41 * rM13) + (lM42 * rM23)) + (lM43 * rM33)) + (lM44 * rM43)
        m.row3.w = (((lM41 * rM14) + (lM42 * rM24)) + (lM43 * rM34)) + (lM44 * rM44)
        return copy.deepcopy(m)

    def determinant(self):
        m11 = self.row0.x
        m12 = self.row0.y
        m13 = self.row0.z
        m14 = self.row0.w
        m21 = self.row1.x
        m22 = self.row1.y
        m23 = self.row1.z
        m24 = self.row1.w
        m31 = self.row2.x
        m32 = self.row2.y
        m33 = self.row2.z
        m34 = self.row2.w
        m41 = self.row3.x
        m42 = self.row3.y
        m43 = self.row3.z
        m44 = self.row3.w
        return ((m11 * m22 * m33 * m44) - (m11 * m22 * m34 * m43) + (m11 * m23 * m34 * m42) - (m11 * m23 * m32 * m44) +
                (m11 * m24 * m32 * m43) - (m11 * m24 * m33 * m42) - (m12 * m23 * m34 * m41) + (m12 * m23 * m31 * m44) -
                (m12 * m24 * m31 * m43) + (m12 * m24 * m33 * m41) - (m12 * m21 * m33 * m44) + (m12 * m21 * m34 * m43) +
                (m13 * m24 * m31 * m42) - (m13 * m24 * m32 * m41) + (m13 * m21 * m32 * m44) - (m13 * m21 * m34 * m42) +
                (m13 * m22 * m34 * m41) - (m13 * m22 * m31 * m44) - (m14 * m21 * m32 * m43) + (m14 * m21 * m33 * m42) -
                (m14 * m22 * m33 * m41) + (m14 * m22 * m31 * m43) - (m14 * m23 * m31 * m42) + (m14 * m23 * m32 * m41))

    def diagonal(self):
        return Vector4(self.row0.x, self.row1.y, self.row2.z, self.row3.w)

    def trace(self):
        return self.row0.x + self.row1.y + self.row2.z + self.row3.w

    def normalize(self):
        d = self.determinant()
        self.row0 /= d
        self.row1 /= d
        self.row2 /= d
        self.row3 /= d

    def normalized(self):
        m = Matrix4(self.row0, self.row1, self.row2, self.row3)
        m.normalize()
        return m

    def invert(self):
        if self.determinant() == 0:
            return Matrix4(self.row0, self.row1, self.row2, self.row3)
        m = self
        inv = Matrix4.identity()
        inv[0] = (m[5] * m[10] * m[15] -
                  m[5] * m[11] * m[14] -
                  m[9] * m[6] * m[15] +
                  m[9] * m[7] * m[14] +
                  m[13] * m[6] * m[11] -
                  m[13] * m[7] * m[10])

        inv[4] = (-m[4] * m[10] * m[15] +
                  m[4] * m[11] * m[14] +
                  m[8] * m[6] * m[15] -
                  m[8] * m[7] * m[14] -
                  m[12] * m[6] * m[11] +
                  m[12] * m[7] * m[10])

        inv[8] = (m[4] * m[9] * m[15] -
                  m[4] * m[11] * m[13] -
                  m[8] * m[5] * m[15] +
                  m[8] * m[7] * m[13] +
                  m[12] * m[5] * m[11] -
                  m[12] * m[7] * m[9])

        inv[12] = (-m[4] * m[9] * m[14] +
                   m[4] * m[10] * m[13] +
                   m[8] * m[5] * m[14] -
                   m[8] * m[6] * m[13] -
                   m[12] * m[5] * m[10] +
                   m[12] * m[6] * m[9])

        inv[1] = (-m[1] * m[10] * m[15] +
                  m[1] * m[11] * m[14] +
                  m[9] * m[2] * m[15] -
                  m[9] * m[3] * m[14] -
                  m[13] * m[2] * m[11] +
                  m[13] * m[3] * m[10])

        inv[5] = (m[0] * m[10] * m[15] -
                  m[0] * m[11] * m[14] -
                  m[8] * m[2] * m[15] +
                  m[8] * m[3] * m[14] +
                  m[12] * m[2] * m[11] -
                  m[12] * m[3] * m[10])

        inv[9] = (-m[0] * m[9] * m[15] +
                  m[0] * m[11] * m[13] +
                  m[8] * m[1] * m[15] -
                  m[8] * m[3] * m[13] -
                  m[12] * m[1] * m[11] +
                  m[12] * m[3] * m[9])

        inv[13] = (m[0] * m[9] * m[14] -
                   m[0] * m[10] * m[13] -
                   m[8] * m[1] * m[14] +
                   m[8] * m[2] * m[13] +
                   m[12] * m[1] * m[10] -
                   m[12] * m[2] * m[9])

        inv[2] = (m[1] * m[6] * m[15] -
                  m[1] * m[7] * m[14] -
                  m[5] * m[2] * m[15] +
                  m[5] * m[3] * m[14] +
                  m[13] * m[2] * m[7] -
                  m[13] * m[3] * m[6])

        inv[6] = (-m[0] * m[6] * m[15] +
                  m[0] * m[7] * m[14] +
                  m[4] * m[2] * m[15] -
                  m[4] * m[3] * m[14] -
                  m[12] * m[2] * m[7] +
                  m[12] * m[3] * m[6])

        inv[10] = (m[0] * m[5] * m[15] -
                   m[0] * m[7] * m[13] -
                   m[4] * m[1] * m[15] +
                   m[4] * m[3] * m[13] +
                   m[12] * m[1] * m[7] -
                   m[12] * m[3] * m[5])

        inv[14] = (-m[0] * m[5] * m[14] +
                   m[0] * m[6] * m[13] +
                   m[4] * m[1] * m[14] -
                   m[4] * m[2] * m[13] -
                   m[12] * m[1] * m[6] +
                   m[12] * m[2] * m[5])

        inv[3] = (-m[1] * m[6] * m[11] +
                  m[1] * m[7] * m[10] +
                  m[5] * m[2] * m[11] -
                  m[5] * m[3] * m[10] -
                  m[9] * m[2] * m[7] +
                  m[9] * m[3] * m[6])

        inv[7] = (m[0] * m[6] * m[11] -
                  m[0] * m[7] * m[10] -
                  m[4] * m[2] * m[11] +
                  m[4] * m[3] * m[10] +
                  m[8] * m[2] * m[7] -
                  m[8] * m[3] * m[6])

        inv[11] = (-m[0] * m[5] * m[11] +
                   m[0] * m[7] * m[9] +
                   m[4] * m[1] * m[11] -
                   m[4] * m[3] * m[9] -
                   m[8] * m[1] * m[7] +
                   m[8] * m[3] * m[5])

        inv[15] = (m[0] * m[5] * m[10] -
                   m[0] * m[6] * m[9] -
                   m[4] * m[1] * m[10] +
                   m[4] * m[2] * m[9] +
                   m[8] * m[1] * m[6] -
                   m[8] * m[2] * m[5])

        det = m[0] * inv[0] + m[1] * inv[4] + m[2] * inv[8] + m[3] * inv[12]
        if det == 0:
            raise RuntimeError
        else:
            det = 1.0 / det
            for i in range(0, 16, 1):
                inv[i] = inv[i] * det

        return inv

    def get_translation(self):
        return self.row3.xyz()

    def get_scale(self):
        return Vector3(self.row0.xyz().length_squared(),
                       self.row1.xyz().length_squared(),
                       self.row2.xyz().length_squared())

    def get_rotation(self, normalized_rows=True):
        row0 = self.row0.xyz()
        row1 = self.row1.xyz()
        row2 = self.row2.xyz()
        if normalized_rows:
            row0.normalize()
            row1.normalize()
            row2.normalize()

        q = Vector4()
        trace = 0.25 * (row0[0] + row1[1] + row2[2] + 1.0)
        if trace > 0:
            sq = math.sqrt(trace)
            q.w = sq
            sq = 1.0 / (4.0 * sq)
            q.x = (row1[2] - row2[1]) * sq
            q.y = (row2[0] - row0[2]) * sq
            q.z = (row0[1] - row1[0]) * sq
        elif row0[0] > row1[1] and row0[0] > row2[2]:
            sq = 2.0 * math.sqrt(1.0 + row0[0] - row1[1] - row2[2])
            q.x = 0.25 * sq
            sq = 1.0 / sq
            q.w = (row2[1] - row1[2]) * sq
            q.y = (row1[0] - row0[1]) * sq
            q.z = (row2[0] - row0[2]) * sq
        elif row1[1] > row2[2]:
            sq = 2.0 * math.sqrt(1.0 + row1[1] - row0[0] - row2[2])
            q.y = 0.25 * sq
            sq = 1.0 / sq
            q.w = (row2[0] - row0[2]) * sq
            q.x = (row1[0] - row0[1]) * sq
            q.z = (row2[1] - row1[2]) * sq
        else:
            sq = 2.0 * math.sqrt(1.0 + row2[2] - row0[0] - row1[1])
            q.z = 0.25 * sq
            sq = 1.0 / sq
            q.w = (row1[0] - row0[1]) * sq
            q.x = (row2[0] - row0[2]) * sq
            q.y = (row2[1] - row1[2]) * sq
        q.normalize()
        return q

    @staticmethod
    def create_translation(v: Vector3):
        m = Matrix4.identity()
        m.row3.x = v.x
        m.row3.y = v.y
        m.row3.z = v.z
        return copy.deepcopy(m)

    @staticmethod
    def create_scale(v: Vector3):
        m = Matrix4.identity()
        m.row0.x = v.x
        m.row1.y = v.y
        m.row2.z = v.z
        return copy.deepcopy(m)

    @staticmethod
    def create_from_axis_angle(axis: Vector3, angle: float):
        m = Matrix4()
        axis.normalize()
        axis_x = axis.x
        axis_y = axis.y
        axis_z = axis.z

        cos = math.cos(-angle)
        sin = math.sin(-angle)
        t = 1.0 - cos

        txx = t * axis_x * axis_x
        txy = t * axis_x * axis_y
        txz = t * axis_x * axis_z
        tyy = t * axis_y * axis_y
        tyz = t * axis_y * axis_z
        tzz = t * axis_z * axis_z

        sin_x = sin * axis_x
        sin_y = sin * axis_y
        sin_z = sin * axis_z

        m.row0.x = txx + cos
        m.row0.y = txy - sin_z
        m.row0.z = txz + sin_y
        m.row0.w = 0
        m.row1.x = txy + sin_z
        m.row1.y = tyy + cos
        m.row1.z = tyz - sin_x
        m.row1.w = 0
        m.row2.x = txz - sin_y
        m.row2.y = tyz + sin_x
        m.row2.z = tzz + cos
        m.row2.w = 0
        m.row3 = Vector4.unit_w()
        return copy.deepcopy(m)

    @staticmethod
    def identity():
        return copy.deepcopy(Matrix4(Vector4.unit_x(), Vector4.unit_y(), Vector4.unit_z(), Vector4.unit_w()))
