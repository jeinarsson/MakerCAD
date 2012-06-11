import unittest
from graph import Graph
from mesh import MeshProvider
from node import Node, NodeParameter, ParameterType, Connector
from makercad.geometry.geometry import Geometry, GeometryType, Box, Union

class TestNodeOutput(unittest.TestCase):
    # Set up a well-working Node object with parameters and connectors.
    # It should automatically compute its output and update it when
    # the parameters or connectors change.
    # The Node.output property is set to None if it cannot be computed
    # and set to something else if it can.

    def setUp(self):
        n = Node()

        #output connector
        c1 = Connector(False, GeometryType.Body3D)
        c1.name = "union of two boxes"
        n.add_connector(c1)

        c2 = Connector(False, GeometryType.Body3D)
        c2.name = "union of box and union"
        n.add_connector(c2)

        #one parameter
        p1 = NodeParameter()
        p1.name = "length"
        p1.datatype = ParameterType.Float
        p1.value = 3.14159

        n.add_parameter(p1)

        def func(inputs, parameters):
            l = parameters["length"]
            b1 = Box(l, l, l)
            b2 = Box(2.*l, 2.*l, 2.*l)
            u1 = Union(b1, b2)
            u2 = Union(u1, b1)

            d = dict()
            d["union of two boxes"] = u1
            d["union of box and union"] = u2
            return d

        n.code = func
        self.n = n

        self.G = Graph(MeshProvider())
        self.G.add_node(n)

    def tearDown(self):
        pass


    def test_parameter_datatype(self):
        # When changing the data type or value of a parameter,
        # the output should be recomputed, and become None
        # if the value and its specified data type do not match.

        n = self.n
        self.assertTrue(None != n.output)

        n.parameters[0].value = 1
        n.parameters[0].value = "a"
        n.parameters[0].value = 1.



if __name__ == '__main__':
    unittest.main()