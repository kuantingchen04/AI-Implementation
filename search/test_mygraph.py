import unittest
import mygraph

class TestQS(unittest.TestCase):
    # graph = {'A':{'B':1}, 'B':{'A':1}}
    # G = Graph(graph)
    def test_load_input(self):
        graph = {'A': {'B': 1}, 'B': {'A': 1}}
        G = mygraph.Graph(graph)

        self.assertEqual(G.V(),2)
        self.assertEqual(G.E(),1)

    def test_add_vertex(self):
        G = mygraph.Graph()
        G.add_vertex('A')
        G.add_vertex('A')
        self.assertEqual(G.V(), 1)
        G.add_vertex('B')
        self.assertEqual(G.V(), 2)
        self.assertEqual(G.degree('A'), 0)
        self.assertEqual(G.degree('B'), 0)

    def test_add_edge(self):
        G = mygraph.Graph()
        G.add_vertex('A')
        G.add_edge('A','B',10)
        self.assertEqual(G.V(), 2)
        self.assertEqual(G.E(), 1)
        self.assertEqual(G.degree('A'), 1)

        G.add_edge('B', 'A', 20)
        self.assertEqual(G.V(), 2)
        self.assertEqual(G.E(), 1)
        self.assertEqual(G.degree('A'), 1)

        G.add_edge('A', 'C', 20)
        self.assertEqual(G.V(), 3)
        self.assertEqual(G.E(), 2)
        self.assertEqual(G.degree('A'), 2)

        G.add_edge('B', 'C', 20)
        self.assertEqual(G.V(), 3)
        self.assertEqual(G.E(), 3)
        self.assertEqual(G.degree('B'), 2)
        self.assertEqual(G.degree('C'), 2)

if __name__ == '__main__':
    unittest.main()