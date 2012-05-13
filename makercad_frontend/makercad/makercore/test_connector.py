import unittest
import graph

class TestGraph(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    
    def test_connection(self):

        def assign_connection(one, another):
            one.connect(another)

        c1 = graph.Connector(True, graph.ConnectorDatatype.Body3D)
        c2 = graph.Connector(False, graph.ConnectorDatatype.Shape2D)
        c3 = graph.Connector(True, graph.ConnectorDatatype.Body3D)

        self.assertRaises(TypeError, c1.connect, "not a Connector object")

        #input (output) cannot connect to input (output)
        self.assertRaises(ValueError, c1.connect, c3)

        #and hence no connectors can connect themselves
        self.assertRaises(ValueError, c1.connect, c1)

        c1.connect(c2) #this should work

        #and then the two connectors should have only each other in links
        self.assertEquals(len(c1.links), 1)
        self.assertTrue(c2 in c1.links)
        self.assertEquals(len(c2.links), 1)
        self.assertTrue(c1 in c2.links)

        self.assertRaises(ValueError, c1.connect, c2) #cannot connect twice
        c2.disconnect(c1) #disconnect...
        c1.connect(c2) #and this should work again
        c1.disconnect(c2) #now disconnect from other side

        #disconnecting again should not be possible
        self.assertRaises(ValueError, c2.disconnect, c1)
        self.assertRaises(ValueError, c1.disconnect, c2)

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