from enum import Enum
from utils.vector import *
from utils.matrix import *
from utils.math import *


class BoneID(Enum):
    Root = 0
    Spine = 1
    Hip = 14
    RightUpperLeg = 16
    RightLowerLeg = 17
    RightFoot = 18
    RightFootToes = 19
    LeftUpperLeg = 21
    LeftLowerLeg = 22
    LeftFoot = 23
    LeftFootToes = 24
    RightShoulder = 4
    RightUpperArm = 5
    RightLowerArm = 6
    RightWrist = 7
    RightRiggedHand = 8
    RightHand = 191
    RightHandIndexUpper = 28
    RightHandIndexLower = 29
    RightHandFingerUpper = 31
    RightHandFingerLower = 32
    RightHandThumb = 25
    LeftShoulder = 9
    LeftUpperArm = 10
    LeftLowerArm = 11
    LeftWrist = 12
    LeftRiggedHand = 13
    LeftHand = 190
    LeftHandIndexUpper = 43
    LeftHandIndexLower = 44
    LeftHandFingerUpper = 46
    LeftHandFingerLower = 47
    LeftHandThumb = 40
    Head = 189
    Jaw = 188
    Unknown63 = 63
    Null = 0xFF


class IKBoneID(Enum):
    Root = 0
    Hip = 1
    Unknown4 = 4
    RightUpperLeg = 5
    RightFootIKTarget = 8
    RightFoot = 9
    Unknown10 = 10
    Unknown11 = 11
    LeftUpperLeg = 12
    Unknown14 = 14
    LeftFootIKTarget = 15
    LeftFoot = 16
    Unknown17 = 17
    Torso = 18
    Unknown19 = 19
    UpperTorsoIKTarget = 20
    Unknown21 = 21
    Unknown22 = 22
    HeadLookAtTarget = 23
    Unknown24 = 24
    RightShoulder = 25
    RightArm = 26
    Unknown27 = 27
    Unknown28 = 28
    RightHandIKTarget = 29
    RightHand = 30
    LeftShoulder = 31
    LeftArm = 32
    Unknown34 = 34
    LeftHandIKTarget = 33
    Unknown35 = 35
    LeftHand = 36
    Unknown37 = 37
    Unknown38 = 38
    Unknown39 = 39
    Unknown40 = 40
    Unknown41 = 41
    Unknown42 = 42
    Null = 0xFF


class ModelNode:

    def __init__(self, model):
        self.model = model
        self.index = 0
        self.id = 0
        self.position = Vector3()
        self.rotation = Vector3()
        self.scale = Vector3()
        self.center = Vector3()
        self.radius = 0.0

        self.child = None
        self.next_sibling = None
        self.parent = None

        self.name = ''

    def get_bone_id(self):
        return BoneID(self.id & 0xFF)

    def get_all_nodes(self, include_siblings=True, include_children=True):
        result = [self]
        if self.child is not None and include_children:
            result.extend(self.child.get_all_nodes())
        if self.next_sibling is not None and include_siblings:
            result.extend(self.next_sibling.get_all_nodes())
        return result

    def get_global_position(self) -> Vector3:
        matrix = self.get_transform_matrix()
        pos = self.center.transformed(matrix)
        return pos

    def get_transform_matrix_self(self) -> Matrix4:
        rot_x = Matrix4.create_from_axis_angle(Vector3.unit_x(), degree_to_radian(self.rotation.x))
        rot_y = Matrix4.create_from_axis_angle(Vector3.unit_y(), degree_to_radian(self.rotation.y))
        rot_z = Matrix4.create_from_axis_angle(Vector3.unit_z(), degree_to_radian(self.rotation.z))
        scale = Matrix4.create_scale(self.scale)
        translate = Matrix4.create_translation(self.position)
        m = scale * rot_x * rot_y * rot_z * translate
        return copy.deepcopy(m)

    def get_transform_matrix(self) -> Matrix4:
        matrix = Matrix4.identity()
        if self.parent is not None:
            matrix = self.parent.get_transform_matrix()
        return self.get_transform_matrix_self() * matrix

    def get_centered_transform_matrix_self(self) -> Matrix4:
        rot_x = Matrix4.create_from_axis_angle(Vector3.unit_x(), self.rotation.x)
        rot_y = Matrix4.create_from_axis_angle(Vector3.unit_y(), self.rotation.y)
        rot_z = Matrix4.create_from_axis_angle(Vector3.unit_z(), self.rotation.z)
        scale = Matrix4.create_scale(self.scale)
        translate = Matrix4.create_translation(self.position)
        center = Matrix4.create_translation(self.center)
        return scale * rot_x * rot_y * rot_z * translate * center

    def get_centered_transform_matrix(self) -> Matrix4:
        matrix = Matrix4.identity()
        if self.parent is not None:
            matrix = self.parent.get_centered_transform_matrix()
        return self.get_centered_transform_matrix_self() * matrix


class Model:

    def __init__(self):
        self.root_node = None


