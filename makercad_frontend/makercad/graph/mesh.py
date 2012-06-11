from PySide import QtCore
from makercad.graph.node import Connector, Node

class MeshProvider(QtCore.QObject):
    """docstring for MeshProvider"""
    def __init__(self):
        super(MeshProvider, self).__init__()
        self._node_ids = dict()
        self._nodes = dict()
        self._node_id_counter = 0
        self._connector_positions = dict()

    def _get_next_node_id(self):
        self._node_id_counter += 1
        return self._node_id_counter

    def register_node(self, node):
        assert isinstance(node, Node)
        assert not node in self._nodes
        node_id = self._get_next_node_id()
        self._node_ids[node] = node_id
        self._nodes[node_id] = node
        self._save_connector_positions(node)
        node.became_dirty.connect(self._handle_dirty_node)
        
    def unregister_node(self, node):
        assert node in self._nodes
        node.became_dirty.disconnect(self._handle_dirty_node)
        self._delete_connector_positions(node)
        node_id = self._node_ids[node]
        del self._node_ids[node]
        del self._nodes[node_id]
        
    def _save_connector_positions(self, node):
        # Save the connector positions for convenience.
        node_id = self._node_ids[node]
        for i, c in enumerate(node.connectors):
            self._connector_positions[c] = (node_id, i)

    def _delete_connector_positions(self, node):
        for c in node.connectors:
            del self._connector_positions[c]

    def register_link(self, conn_1, conn_2):
        assert conn_1.is_input ^ conn_2.is_input
        if conn_1.is_input:
            conn_input, conn_output = conn_1, conn_2
        else:
            conn_input, conn_output = conn_2, conn_1

        pos_input = self._connector_positions[conn_input]
        pos_output = self._connector_positions[conn_output]

    def unregister_link(self, conn_1, conn_2):
        assert conn_1.is_input ^ conn_2.is_input
        if conn_1.is_input:
            conn_input, conn_output = conn_1, conn_2
        else:
            conn_input, conn_output = conn_2, conn_1

        pos_input = self._connector_positions[conn_input]
        pos_output = self._connector_positions[conn_output]

    def _get_operations_recursive(self, output):
        operations = set()
        if 0 == len(output):
            return operations

        for key in output:
            item = output[key]
            operations.add(item)
            children = self._get_operations_recursive(item.inputs)
            operations = operations.union(children)

        return operations

    def _get_geometry_message(self, output):
        # First assemble a directed graph of makercad geometry operations.
        nodes = self._get_operations_recursive(output)
        node_numbers = dict()
        for (i, n) in enumerate(nodes):
            node_numbers[n] = i

        # Then build a message
        msg = ""
        for n in nodes:
            children_nums = [node_numbers[n.inputs[key]] for key in n.inputs]
            msg += "  " + str(node_numbers[n]) + ": " + str(n) + ", inputs "
            for child_num in children_nums:
                msg += str(child_num) + " "
            msg += "\n"

        return msg

    def _handle_dirty_node(self, node, updated):
        if updated:
            # The node update might be a change of connectors, so we
            # need to update the list.
            self._save_connector_positions(node)

        if None != node.output:
            msg = self._get_geometry_message(node.output)
        else:
            msg = "Output is None."

        for c in node.connectors:
            (node_id, i) = self._connector_positions[c]
            c.mesh = "Mesh for node {0}, connector {1}, revision {2}.\n{3}".\
                format(node_id, i, node.revision, msg)