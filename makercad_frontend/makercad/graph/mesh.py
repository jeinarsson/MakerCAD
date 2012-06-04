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

    def _get_execution_message(node_output):
        raise NotImplementedError

    def _get_next_node_id(self):
        self._node_id_counter += 1
        return self._node_id_counter

    def register_node(self, node):
        assert isinstance(node, Node)
        assert not node in self._nodes
        node_id = self._get_next_node_id()
        self._node_ids[node] = node_id
        self._nodes[node_id] = node
        self.save_connector_positions(node)
        node.updated_output.connect(self._handle_updated_node)
        node.became_dirty.connect(self._handle_dirty_node)
        
    def unregister_node(self, node):
        assert node in self._nodes
        node.updated_output.disconnect(self._handle_updated_node)
        node.became_dirty.disconnect(self._handle_dirty_node)
        self.delete_connector_positions(node)
        node_id = self._node_ids[node]
        del self._node_ids[node]
        del self._nodes[node_id]
        
    def save_connector_positions(self, node):
        # Save the connector positions for convenience.
        node_id = self._node_ids[node]
        for i, c in enumerate(node.connectors):
            self._connector_positions[c] = (node_id, i)

    def delete_connector_positions(self, node):
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


    def _handle_updated_node(self, node):
        # The node update might be a change of connectors, so we
        # need to update the list.
        self.save_connector_positions(node)
        raise NotImplementedError

    def _handle_dirty_node(self, node):
        raise NotImplementedError
        