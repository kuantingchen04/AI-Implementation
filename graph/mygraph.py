import csv

"""Graph API implementation"""


class Graph:
    """Graph data type"""

    def __init__(self, g_dict=None):  # create an empty graph
        self.cnt_V = 0  # number of vertices
        self.cnt_E = 0  # number of edges
        self.g_dict = {}  # store vertices adjacent to v, adj = { v1:{ va:10,vb:5 } , v2:{vc:10} }
        if g_dict:
            self.g_dict = g_dict
            self.cnt_V = len(g_dict.keys())
            self.cnt_E = len([1 for x in g_dict.values()
                              for _ in x.keys()]) / 2

    def V(self):
        return self.cnt_V

    def E(self):
        return self.cnt_E

    def add_vertex(self, v):
        """Add vertex v if not exist"""
        if v not in self.g_dict:
            self.g_dict[v] = {}
            self.cnt_V += 1

    def add_edge(self, v, w, cost):
        """Add an edge v-w"""
        self.add_vertex(v)
        self.add_vertex(w)
        if w in self.g_dict[v]:
            return
        self.g_dict[v][w] = cost
        self.g_dict[w][v] = cost

        self.cnt_E += 1

    def get_dict(self):
        return self.g_dict

    def degree(self, v):
        return len(self.g_dict[v].keys())


def main(G, input_file):
    """Run add"""
    with open(input_file, 'r') as f:
        csv_reader = csv.reader(f)
        for line in csv_reader:
            [v, w, cost] = line[0], line[1], int(line[2])
            G.add_edge(v, w, cost)

if __name__ == '__main__':

    G = Graph() # construct a graph instance G
    INPUT_FILE = "graph.txt"
    main(G, INPUT_FILE) # read graph.txt into G
    print "number of vertices: %s" % G.V()
    print "number of edges: %s" % G.E()