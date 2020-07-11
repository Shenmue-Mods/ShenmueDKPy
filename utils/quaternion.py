import math
import copy
from utils.vector import *


def quat_from_euler(angles):
    rotation_x = angles.z * 0.5
    rotation_y = angles.y * 0.5
    rotation_z = angles.z * 0.5

    c1 = math.cos(rotation_x)
    c2 = math.cos(rotation_y)
    c3 = math.cos(rotation_z)
    s1 = math.sin(rotation_x)
    s2 = math.sin(rotation_y)
    s3 = math.sin(rotation_z)

    quat = Vector4()
    quat.w = c1 * c2 * c3 - s1 * s2 * s3
    quat.x = s1 * c2 * c3 + c1 * s2 * s3
    quat.y = c1 * s2 * c3 - s1 * c2 * s3
    quat.z = c1 * c2 * s3 + s1 * s2 * c3
    return copy.deepcopy(quat)


def quat_from_axis(axis: Vector3, angle: float):
    if axis.length_squared() == 0.0:
        return Vector4.unit_w()
    angle *= 0.5
    norm_axis = axis.normalized()
    xyz = norm_axis * math.sin(angle)
    quat = Vector4()
    quat.x = xyz.x
    quat.y = xyz.y
    quat.z = xyz.z
    quat.w = math.cos(angle)
    return copy.deepcopy(quat)


def quat_multiply(lhs: Vector4, rhs: Vector4):
    xyz = lhs.xyz() * rhs.w + rhs.xyz() * lhs.w + Vector3.cross(lhs.xyz(), rhs.xyz())
    w = lhs.w * rhs.w - Vector3.dot(lhs.xyz(), rhs.xyz())
    return copy.deepcopy(Vector4(xyz.x, xyz.y, xyz.z, w))


def axis_angle_from_quat(quat: Vector4):
    q = quat
    if math.fabs(q.w) > 1.0:
        q.normalize()
    result = Vector4()
    result.w = 2.0 * math.acos(q.w)
    den = math.sqrt(1.0 - q.w * q.w)
    if den > 0.0001:
        result.x = q.x / den
        result.y = q.y / den
        result.z = q.z / den
    else:
        result.x = 1.0
        result.y = 0.0
        result.z = 0.0
    return copy.deepcopy(result)