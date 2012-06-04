import unittest
from node import Node, NodeParameter, ParameterType, Connector
from makercad.geometry import Geometry, GeometryType

class TestNodeOutput(unittest.TestCase):
    # Set up a well-working Node object with parameters and connectors.
    # It should automatically compute its output and update it when
    # the parameters or connectors change.
    # The Node.output property is set to None if it cannot be computed
    # and set to something else if it can.

    def setUp(self):
        n = Node()

        #input connector
        c1 = Connector(True, GeometryType.Body3D)
        c1.name = "input connector name"
        n.add_connector(c1)

        #output connector
        c2 = Connector(False, GeometryType.Shape2D)
        c2.name = "output connector name"
        n.add_connector(c2)

        #two parameters
        p1 = NodeParameter()
        p1.name = "integer parameter name"
        p1.datatype = ParameterType.Integer
        p1.value = 3

        p2 = NodeParameter()
        p2.name = "float parameter name"
        p2.datatype = ParameterType.Float
        p2.value = 3.14159

        n.add_parameter(p1)
        n.add_parameter(p2)

        def func(inputs, parameters):
            d = dict()
            g = Geometry()
            g._datatype = GeometryType.Shape2D
            d["output connector name"] = g
            return d

        n.code = func
        self.n = n

    def tearDown(self):
        pass


    def test_parameter_datatype(self):
        # When changing the data type or value of a parameter,
        # the output should be recomputed, and become None
        # if the value and its specified data type do not match.

        n = self.n
        self.assertTrue(None != n.output)

        n.parameters[0].datatype = ParameterType.Float
        n.parameters[0].value = 1
        self.assertTrue(None == n.output)

        n.parameters[0].value = 1.
        self.assertTrue(None != n.output)

        # But if we remove the parameter from the node,
        # the node should not care whether the parameter changes value
        p = n.parameters[0]
        n.remove_parameter(p)
        p.value = 1
        self.assertTrue(None != n.output)



if __name__ == '__main__':
    unittest.main()