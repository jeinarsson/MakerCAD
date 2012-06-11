import unittest
from makercad.graph.graph import Graph
from makercad.graph.node import Node, Connector
from makercad.geometry.geometry import GeometryType
from mesh import MeshProvider

class TestGraph(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def test_connection(self):

        c11 = Connector(True, GeometryType.Body3D)
        c12 = Connector(False, GeometryType.Shape2D)
        c21 = Connector(True, GeometryType.Body3D)

        n1 = Node()
        n1.add_connector(c11)
        n1.add_connector(c12)

        n2 = Node()
        n2.add_connector(c21)

        G = Graph(MeshProvider())
        G.add_node(n1)
        G.add_node(n2)

        self.assertRaises(AssertionError, G.add_link, c11, "not a Connector object")

        #input (output) cannot link to input (output)
        self.assertRaises(AssertionError, G.add_link, c11, c21)

        #and hence no connectors can link themselves
        self.assertRaises(AssertionError, G.add_link, c12, c12)

        #there should be no links now
        self.assertEquals(len(G.links), 0)

        G.add_link(c12, c21) #this should work

        #and then there should be one link now
        self.assertEquals(len(G.links), 1)

        self.assertRaises(AssertionError, G.add_link, c12, c21) #cannot link twice
        G.remove_link(c21, c12)

        #unlinking twice should not be possible
        self.assertRaises(AssertionError, G.remove_link, c21, c12)

        G.add_link(c12, c21) #and this should work again        


    def test_input(self):    

        def assign_input(c, value):
            c.is_input = value

        #create one input connector
        c1 = Connector(True, GeometryType.Body3D)
        self.assertTrue(c1.is_input)

        #and one output connector
        c2 = Connector(False, GeometryType.Body3D)
        self.assertTrue(not c2.is_input)

        #Try to assign the to the is_input values of the connectors
        self.assertRaises(AttributeError, assign_input, c1, False)
        self.assertRaises(AttributeError, assign_input, c2, False)

        



if __name__ == '__main__':
    unittest.main()