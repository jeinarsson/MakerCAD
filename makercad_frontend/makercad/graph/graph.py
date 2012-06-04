from PySide import QtCore
import collections
from node import Node, Connector

def is_acyclic(A):
    """
    Determines whether an adjacency matrix A is acyclic.

    The matrix is represented as a list of lists, such that
    A_{ij} = A[i][j], i.e. each row in the matrix is a sub-list.

    The matrix should be square and contain only boolean values.
    """

    # Find out if the graph is cyclic by trying to do a topological sorting
    # of the graph. If it's impossible to find one, the graph has cycles.

    # In fact, we do the topological "backwards", i.e. first picking out
    # the leaf nodes and finally finding the root nodes. This admits a pretty
    # convenient handling of all the lists.

    # First take a copy of the adjacency matrix.
    A = [list(row) for row in A]
    N = len(A)

    # Find all nodes with no outgoing edge.
    S = list()
    for i, row in enumerate(A):
        assert N == len(row)
        if not True in row:
            S.append(i)

    # Take a node with no outgoing edges.
    while len(S) > 0:
        j = S.pop()
        # Go through and remove any edges to the node.
        # If this leads to a linking node having no edges left, add it to S.
        for i, row in enumerate(A):
            if True == row[j]:
                row[j] = False
                if not True in row:
                    S.append(i)

    for row in A:
        if True in row:
            # There are edges left => the graph has cycles.
            return False

    # There are no edges left => graph is acyclic.
    return True


class Graph(QtCore.QObject):
    """docstring for Graph"""
    def __init__(self, mesh_provider):
        super(Graph, self).__init__()
        self._links = set()
        self._nodes = set()
        self._mesh_provider = mesh_provider

    def get_links(self):
        return frozenset(self._links)
    links = property(get_links)

    def add_link(self, conn_1, conn_2):
        assert isinstance(conn_1, Connector)
        assert isinstance(conn_2, Connector)
        assert (conn_1.is_input ^ conn_2.is_input), \
            "connection needs one output and one input"

        if conn_1.is_input:
            input_node, output_node = conn_1.node, conn_2.node
        else:
            input_node, output_node = conn_2.node, conn_1.node

        output_node.became_dirty.connect(input_node.set_dirty)

        link = frozenset((conn_1, conn_2))
        assert not link in self._links
        self._links.add(link)

        self._mesh_provider.register_link(conn_1, conn_2)

    def remove_link(self, conn_1, conn_2):
        link = frozenset((conn_1, conn_2))
        assert link in self._links

        if conn_1.is_input:
            input_node, output_node = conn_1.node, conn_2.node
        else:
            input_node, output_node = conn_2.node, conn_1.node

        output_node.became_dirty.disconnect(input_node.set_dirty)
        self._mesh_provider.unregister_link(conn_1, conn_2)

        self._links.remove(link)

    def get_nodes(self):
        return frozenset(self._nodes)
    nodes = property(get_nodes)

    def add_node(self, node):
        assert not node in self._nodes
        self._nodes.add(node)        
        self._mesh_provider.register_node(node)

    def remove_node(self, node):
        self._mesh_provider.unregister_node(node)
        self._nodes.remove(node)
        
