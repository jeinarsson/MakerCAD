import unittest
import graph

class TestAcyclic(unittest.TestCase):
    # Set up a well-working Node object with parameters and connectors.
    # It should automatically compute its output and update it when
    # the parameters or connectors change.
    # The Node.output property is set to None if it cannot be computed
    # and set to something else if it can.

    def setUp(self):
        pass

    def tearDown(self):
        pass


    def test_is_acyclic(self):
        A = [[False, True, False],
             [False, False, True],
             [False, False, False]]

        self.assertTrue(graph.is_acyclic(A))

        A[2][0] = True
        self.assertTrue(not graph.is_acyclic(A))
        

if __name__ == '__main__':
    unittest.main()