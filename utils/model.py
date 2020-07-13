from enum import Enum
from utils.vector import *
from utils.matrix import *
from utils.math import *


class BoneID(Enum):
    Root = 0
    Spine = 1
    Hip = 14
    UpperLeg_R = 16
    LowerLeg_R = 17
    Foot_R = 18
    FootToes_R = 19
    UpperLeg_L = 21
    LowerLeg_L = 22
    Foot_L = 23
    FootToes_L = 24
    Shoulder_R = 4
    UpperArm_R = 5
    LowerArm_R = 6
    Wrist_R = 7
    RiggedHand_R = 8
    Hand_R = 191
    HandIndexUpper_R = 28
    HandIndexLower_R = 29
    HandFingerUpper_R = 31
    HandFingerLower_R = 32
    HandThumb_R = 25
    Shoulder_L = 9
    UpperArm_L = 10
    LowerArm_L = 11
    Wrist_L = 12
    RiggedHand_L = 13
    Hand_L = 190
    HandIndexUpper_L = 43
    HandIndexLower_L = 44
    HandFingerUpper_L = 46
    HandFingerLower_L = 47
    HandThumb_L = 40
    Head = 189
    Jaw = 188
    Unknown63 = 63
    Null = 0xFF


class IKBoneID(Enum):
    Root = 0
    Hip = 1
    Unknown4 = 4
    UpperLeg_R = 5
    FootIKTarget_R = 8
    Foot_R = 9
    Unknown10 = 10
    Unknown11 = 11
    UpperLeg_L = 12
    Unknown14 = 14
    FootIKTarget_L = 15
    Foot_L = 16
    Unknown17 = 17
    Torso = 18
    Unknown19 = 19
    UpperTorsoIKTarget = 20
    Unknown21 = 21
    Unknown22 = 22
    HeadLookAtTarget = 23
    Unknown24 = 24
    Shoulder_R = 25
    Arm_R = 26
    Unknown27 = 27
    Unknown28 = 28
    HandIKTarget_R = 29
    Hand_R = 30
    Shoulder_L = 31
    Arm_L = 32
    Unknown34 = 34
    HandIKTarget_L = 33
    Unknown35 = 35
    Hand_L = 36
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


