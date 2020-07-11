from files.file import File
from utils.model import *
from utils.stream_helper import *
from utils.math import *


# only need the node data for armature creation, so no mesh reading (for now)

class MT5(File, Model):

    class Mesh:

        def __init__(self, node, binary_stream=None, base_offset=None):
            self.node = node
            self.poly_type = 0
            self.vertices_offset = 0
            self.vertex_count = 0
            self.faces_offset = 0
            self.center_x = 0.0
            self.center_y = 0.0
            self.center_z = 0.0
            self.radius = 0.0

            if binary_stream:
                self.read(binary_stream, base_offset)

        def read(self, binary_stream, base_offset):
            self.poly_type = sread_uint(binary_stream)
            self.vertices_offset = sread_uint(binary_stream)
            self.vertex_count = sread_int(binary_stream)
            self.faces_offset = sread_uint(binary_stream)
            self.center_x = sread_float(binary_stream)
            self.center_y = sread_float(binary_stream)
            self.center_z = sread_float(binary_stream)
            self.radius = sread_float(binary_stream)

    class Node(ModelNode):

        def __init__(self, model, parent=None, binary_stream=None, base_offset=None):
            super().__init__(model)
            self.id = 0
            self.mesh_offset = 0
            self.rot_x = 0
            self.rot_y = 0
            self.rot_z = 0
            self.scl_x = 0.0
            self.scl_y = 0.0
            self.scl_z = 0.0
            self.pos_x = 0.0
            self.pos_y = 0.0
            self.pos_z = 0.0
            self.child_node_offset = 0
            self.next_node_offset = 0
            self.parent_node_offset = 0
            self.name = 0
            self.unknown = 0

            self.parent = parent
            if binary_stream:
                self.read(binary_stream, base_offset)

        def read(self, binary_stream, base_offset):
            self.id = sread_uint(binary_stream)
            self.mesh_offset = sread_uint(binary_stream)
            self.rot_x = sread_uint(binary_stream)
            self.rot_y = sread_uint(binary_stream)
            self.rot_z = sread_uint(binary_stream)
            self.scl_x = sread_float(binary_stream)
            self.scl_y = sread_float(binary_stream)
            self.scl_z = sread_float(binary_stream)
            self.pos_x = sread_float(binary_stream)
            self.pos_y = sread_float(binary_stream)
            self.pos_z = sread_float(binary_stream)
            self.child_node_offset = sread_uint(binary_stream)
            self.next_node_offset = sread_uint(binary_stream)
            self.parent_node_offset = sread_uint(binary_stream)
            self.name = sread_uint(binary_stream)
            self.unknown = sread_uint(binary_stream)

            self.position = Vector3(self.pos_x, self.pos_y, self.pos_z)
            self.scale = Vector3(self.scl_x, self.scl_y, self.scl_z)
            self.rotation = Vector3(short_to_degree(self.rot_x), short_to_degree(self.rot_y), short_to_degree(self.rot_z))

            if self.mesh_offset != 0:
                binary_stream.seek(base_offset + self.mesh_offset)
                mesh = MT5.Mesh(self, binary_stream, base_offset)
                self.center = Vector3(mesh.center_x, mesh.center_y, mesh.center_z)

            if self.child_node_offset:
                binary_stream.seek(base_offset + self.child_node_offset)
                self.child = MT5.Node(self.model, self, binary_stream, base_offset)

            if self.next_node_offset:
                binary_stream.seek(base_offset + self.next_node_offset)
                self.next_sibling = MT5.Node(self.model, self.parent, binary_stream, base_offset)

    class Header:

        def __init__(self):
            self.signature = 0
            self.node_size = 0
            self.first_node_offset = 0

        def read(self, binary_stream):
            self.signature = sread_uint(binary_stream)
            self.node_size = sread_uint(binary_stream)
            self.first_node_offset = sread_uint(binary_stream)

    def __init__(self):
        super().__init__()
        self.header = self.Header()

    def _read(self, binary_stream):
        self.header.read(binary_stream)

        binary_stream.seek(self.base_offset + self.header.first_node_offset)
        self.root_node = MT5.Node(self, None, binary_stream, self.base_offset)
        return True

    def _write(self, binary_stream):
        return True

    def _clean(self):
        return True
