import unittest
import graph

class TestNode(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass


    def test_code(self):
        n = graph.Node()
        p1 = graph.NodeParameter()
        p1.name = "parameter_1"
        p1.value = 1

        p2 = graph.NodeParameter()
        p2.name = "test param"
        p2.value = "original value"

        def func(**kwargs):
            for k in kwargs.keys():
                if isinstance(kwargs[k], int):
                    kwargs[k] += 1
                if isinstance(kwargs[k], str):
                    kwargs[k] += " changed"
            return kwargs

        def assign_code(node, code):
            node.code = code

        self.assertRaises(Exception, assign_code, n, "a string")

        n.code = func

        n.add_parameter(p1)

        n.add_parameter(p2)

        d = n.compute_output()
        self.assertTrue(d["parameter_1"] == 2)
        self.assertTrue(d["test param"] == "original value changed")


    def test_input(self):    

        def assign_input(c, value):
            c.is_input = value

        c1 = graph.Connector(True, graph.ConnectorDatatype.Body3D)
        c2 = graph.Connector(False, graph.ConnectorDatatype.Body3D)

        self.assertTrue(c1.is_input)
        self.assertTrue(not c2.is_input)
        self.assertRaises(AttributeError, assign_input, c1, False)
        self.assertRaises(AttributeError, assign_input, c2, False)



if __name__ == '__main__':
    unittest.main()