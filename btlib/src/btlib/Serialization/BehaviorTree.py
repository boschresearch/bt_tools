# automatically generated by the FlatBuffers compiler, do not modify

# namespace: Serialization

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()


class BehaviorTree(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsBehaviorTree(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = BehaviorTree()
        x.Init(buf, n + offset)
        return x

    # BehaviorTree
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # BehaviorTree
    def RootUid(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.Get(
                flatbuffers.number_types.Uint16Flags, o +
                self._tab.Pos)
        return 0

    # BehaviorTree
    def Nodes(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 4
            x = self._tab.Indirect(x)
            from btlib.Serialization.TreeNode import TreeNode
            obj = TreeNode()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # BehaviorTree
    def NodesLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # BehaviorTree
    def NodesIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        return o == 0

    # BehaviorTree
    def NodeModels(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 4
            x = self._tab.Indirect(x)
            from btlib.Serialization.NodeModel import NodeModel
            obj = NodeModel()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # BehaviorTree
    def NodeModelsLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # BehaviorTree
    def NodeModelsIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        return o == 0


def BehaviorTreeStart(builder):
    builder.StartObject(3)


def BehaviorTreeAddRootUid(
        builder, rootUid):
    builder.PrependUint16Slot(0, rootUid, 0)


def BehaviorTreeAddNodes(builder, nodes):
    builder.PrependUOffsetTRelativeSlot(
        1, flatbuffers.number_types.UOffsetTFlags.py_type(nodes), 0)


def BehaviorTreeStartNodesVector(
        builder, numElems):
    return builder.StartVector(4, numElems, 4)


def BehaviorTreeAddNodeModels(builder, nodeModels):
    builder.PrependUOffsetTRelativeSlot(
        2, flatbuffers.number_types.UOffsetTFlags.py_type(nodeModels), 0)


def BehaviorTreeStartNodeModelsVector(
        builder, numElems):
    return builder.StartVector(4, numElems, 4)


def BehaviorTreeEnd(builder):
    return builder.EndObject()
