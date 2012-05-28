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
    def __init__(self):
        super(Graph, self).__init__()
        self._links = set()
        self._nodes = dict()
        self._node_ids = dict()
        self._node_id_counter = 0

    def _get_next_node_id(self):
        self._node_id_counter += 1
        return self._node_id_counter

    def get_links(self):
        return frozenset(self._links)
    links = property(get_links)

    def add_link(self, conn_1, conn_2):
        assert isinstance(conn_1, Connector)
        assert isinstance(conn_2, Connector)
        assert (conn_1.is_input ^ conn_2.is_input), \
            "connection needs one output and one input"
        link = frozenset((conn_1, conn_2))
        assert not link in self._links
        self._links.add(link)    
    def remove_link(self, conn_1, conn_2):
        link = frozenset((conn_1, conn_2))
        assert link in self._links
        self._links.remove(link)

    def get_nodes(self):
        return frozenset(self._nodes)
    nodes = property(get_nodes)

    def add_node(self, node):
        assert isinstance(node, Node)
        assert not node in self._nodes
        node_id = self._get_next_node_id()
        self._node_ids[node] = node_id
        self._nodes[node_id] = node

    def remove_node(self, node):
        assert node in self._nodes
        node_id = self._node_ids[node]
        del self._node_ids[node]
        del self._nodes[node_id]

    def get_node(self, node_id):
        return self._nodes[node_id]
      
       