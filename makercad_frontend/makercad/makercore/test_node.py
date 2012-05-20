import unittest
import graph

class TestNode(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass


    def test_parameters_and_connections(self):
        n = graph.Node()

        c1 = graph.Connector(True, graph.GeometryType.Body3D)
        n.add_connector(c1)

        #a connector may not be added twice to a node
        self.assertRaises(ValueError, n.add_connector, c1)

        c2 = graph.Connector(False, graph.GeometryType.Body3D)
        n.add_connector(c2)

        self.assertTrue(2 == len(n.connectors))
        # n.remove_connector(c1)
        # self.assertTrue(1 == len(n.connectors))

        self.assertTrue(not n._is_output_computable())

        c1.name = "connector name 1"
        c2.name = "connector name 2"
        def func(connectors, parameters):
                d = dict()
                x = graph.Geometry()
                x._datatype = graph.GeometryType.Body3D
                d["connector name 2"] = x
                return d

        #should not work yet since there is no code set
        self.assertRaises(Exception, n._update_output)
        
        n.code = func
        #should work now
        n._update_output()

        p1 = graph.NodeParameter()
        p1.name = "parameter name"
        p1.datatype = graph.ParameterType.Float
        p1.value = 1.
        n.add_parameter(p1)

        #this should work
        n._update_output()

        #should not work since datatype is wrong
        p1.value = 1
        self.assertRaises(Exception, n._update_output)

        #should work again
        p1.value = 1.
        n._update_output()

        #should not work since datatype is wrong
        p1.value = None
        self.assertRaises(Exception, n._update_output)

        #should work again
        p1.value = 1.
        n._update_output()
        
        #should not work since datatype is wrong
        p1.datatype = graph.ParameterType.Integer
        self.assertRaises(Exception, n._update_output)

        #should work again
        p1.value = 3
        n._update_output()

        #should not work since parameter is unnamed
        p1.name = None
        self.assertRaises(Exception, n._update_output)

    def function():
        pass





if __name__ == '__main__':
    unittest.main()