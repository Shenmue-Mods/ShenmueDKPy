#!/usr/bin/python3

import sys
sys.path.append(".")

from files.animation.motn import MOTN
from files.models.mt5 import MT5

if __name__ == '__main__':

    filename = 'H:\\Projects\\Programming\\Shenmue\\ShenmueData\\UTest\\cold.mot'
    motnFile = MOTN()
    motnFile.read(filename)
    print(len(motnFile.sequences))

    #filename = 'H:\\Projects\\Programming\\Shenmue\\ShenmueData\\UTest\\yka_m.mt5'
    #mt5File = MT5()
    #mt5File.read(filename)

    #nodes = mt5File.root_node.get_all_nodes()

    #print(len(nodes))
    #print(nodes)

    #for node in nodes:
    #    print(node.get_bone_id())
    #    print(node.center.transformed(node.get_transform_matrix()))
    #    print(node.get_transform_matrix())

