import math
import copy


class Vector3:

    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return '(' + str(self.x) + ' , ' + str(self.y) + ' , ' + str(self.z) + ')'

    def __getitem__(self, key):
        if key == 0:
            return self.x
        if key == 1:
            return self.y
        if key == 2:
            return self.z
        raise IndexError()

    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        if key == 1:
            self.y = value
        if key == 2:
            self.z = value
        raise IndexError()

    def __neg__(self):
        self.x = -self.x
        self.y = -self.y
        self.z = -self.z
        return self

    def __add__(self, other):
        if other is Vector4:
            self.x += other.x
            self.y += other.y
            self.z += other.z
        elif other is int or float:
            self.x += other
            self.y += other
            self.z += other
        return self

    def __sub__(self, other):
        if other is Vector4:
            self.x -= other.x
            self.y -= other.y
            self.z -= other.z
        elif other is int or float:
            self.x -= other
            self.y -= other
            self.z -= other
        return self

    def __mul__(self, other):
        if other is Vector4:
            self.x *= other.x
            self.y *= other.y
            self.z *= other.z
        elif other is int or float:
            self.x *= other
            self.y *= other
            self.z *= other
        return self

    def __truediv__(self, other):
        if other is Vector4:
            self.x /= other.x
            self.y /= other.y
            self.z /= other.z
        elif other is int or float:
            self.x /= other
            self.y /= other
            self.z /= other
        return self

    def length(self):
        return math.sqrt(self.x * self.x +
                         self.y * self.y +
                         self.z * self.z)

    def length_squared(self):
        return (self.x * self.x +
                self.y * self.y +
                self.z * self.z)

    def normalize(self):
        scale = 1.0 / self.length()
        self.x *= scale
        self.y *= scale
        self.z *= scale

    def normalized(self):
        v = Vector3(self.x, self.y, self.z)
        v.normalize()
        return copy.deepcopy(v)

    def transform(self, matrix):
        x = (self.x * matrix.row0.x +
             self.y * matrix.row1.x +
             self.z * matrix.row2.x +
             matrix.row3.x)
        y = (self.x * matrix.row0.y +
             self.y * matrix.row1.y +
             self.z * matrix.row2.y +
             matrix.row3.y)
        z = (self.x * matrix.row0.z +
             self.y * matrix.row1.z +
             self.z * matrix.row2.z +
             matrix.row3.z)
        self.x = x
        self.y = y
        self.z = z

    def transformed(self, matrix):
        v = Vector3(self.x, self.y, self.z)
        v.transform(matrix)
        return copy.deepcopy(v)

    @staticmethod
    def cross(lhs, rhs):
        out = Vector3()
        out.x = lhs.y * rhs.z - lhs.z * rhs.y
        out.y = lhs.z * rhs.x - lhs.x * rhs.z
        out.z = lhs.x * rhs.y - lhs.y * rhs.x
        return copy.deepcopy(out)

    @staticmethod
    def dot(lhs, rhs):
        return lhs.x * rhs.x + lhs.y * rhs.y + lhs.z * rhs.z

    @staticmethod
    def unit_x():
        return copy.deepcopy(Vector3(1.0, 0.0, 0.0))

    @staticmethod
    def unit_y():
        return copy.deepcopy(Vector3(0.0, 1.0, 0.0))

    @staticmethod
    def unit_z():
        return copy.deepcopy(Vector3(0.0, 0.0, 1.0))


class Vector4:

    def __init__(self, x=0.0, y=0.0, z=0.0, w=0.0):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __str__(self):
        return '(' + str(self.x) + ' , ' + str(self.y) + ' , ' + str(self.z) + ' , ' + str(self.w) + ')'

    def __getitem__(self, key):
        if key == 0:
            return self.x
        if key == 1:
            return self.y
        if key == 2:
            return self.z
        if key == 3:
            return self.w
        raise IndexError()

    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        if key == 1:
            self.y = value
        if key == 2:
            self.z = value
        if key == 3:
            self.w = value
        raise IndexError()

    def __neg__(self):
        self.x = -self.x
        self.y = -self.y
        self.z = -self.z
        self.w = -self.w
        return self

    def __add__(self, other):
        if other is Vector4:
            self.x += other.x
            self.y += other.y
            self.z += other.z
            self.w += other.w
        elif other is int or float:
            self.x += other
            self.y += other
            self.z += other
            self.w += other
        return self

    def __sub__(self, other):
        if other is Vector4:
            self.x -= other.x
            self.y -= other.y
            self.z -= other.z
            self.w -= other.w
        elif other is int or float:
            self.x -= other
            self.y -= other
            self.z -= other
            self.w -= other
        return self

    def __mul__(self, other):
        if other is Vector4:
            self.x *= other.x
            self.y *= other.y
            self.z *= other.z
            self.w *= other.w
        elif other is int or float:
            self.x *= other
            self.y *= other
            self.z *= other
            self.w *= other
        return self

    def __truediv__(self, other):
        if other is Vector4:
            self.x /= other.x
            self.y /= other.y
            self.z /= other.z
            self.w /= other.w
        elif other is int or float:
            self.x /= other
            self.y /= other
            self.z /= other
            self.w /= other
        return self

    def xyz(self):
        return Vector3(self.x, self.y, self.z)

    def length(self):
        return math.sqrt(self.x * self.x +
                         self.y * self.y +
                         self.z * self.z +
                         self.w * self.w)

    def length_squared(self):
        return (self.x * self.x +
                self.y * self.y +
                self.z * self.z +
                self.w * self.w)

    def normalize(self):
        scale = 1.0 / self.length()
        self.x *= scale
        self.y *= scale
        self.z *= scale
        self.w *= scale

    def normalized(self):
        v = Vector4(self.x, self.y, self.z, self.w)
        v.normalize()
        return copy.deepcopy(v)

    @staticmethod
    def unit_x():
        return copy.deepcopy(Vector4(1.0, 0.0, 0.0, 0.0))

    @staticmethod
    def unit_y():
        return copy.deepcopy(Vector4(0.0, 1.0, 0.0, 0.0))

    @staticmethod
    def unit_z():
        return copy.deepcopy(Vector4(0.0, 0.0, 1.0, 0.0))

    @staticmethod
    def unit_w():
        return copy.deepcopy(Vector4(0.0, 0.0, 0.0, 1.0))
