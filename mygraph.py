from quicksort.quicksort import quicksort
"""Graph API implementation"""


class Graph:
    """Graph data type"""

    def __init__(self, g_dict=None):  # create an empty graph
        self.cnt_V = 0  # number of vertices
        self.cnt_E = 0  # number of edges
        self.g_dict = {}  # store vertices adjacent to v, adj = { v1:{ va:10,vb:5 } , v2:{vc:10} }
        if g_dict:
            self.g_dict = g_dict
            self.cnt_V = len(list(g_dict.keys()))
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

    def get_nodes(self):
        return list(self.g_dict.keys())

    def get_cost(self, v, w):
        return self.g_dict[v][w]

    def degree(self, v):
        return len(list(self.g_dict[v].keys()))

    def adj(self, v):
        return list(self.g_dict[v].keys())

    def get_edges(self):
        edges = []
        node_idx = {x: i for i, x in enumerate(self.get_nodes())}
        for v, value in self.g_dict.iteritems():
            for w, cost in value.iteritems():
                if (cost, w, v) not in edges:
                    edges.append((cost, node_idx[v], node_idx[w]))
        return quicksort(edges)

    def mst(self):
        """Minimum spanning tree"""
        def find(parent, i):
            if parent[i] == i:
                return i
            return find(parent, parent[i])

        def union(parent, rank, x, y):
            x_root = find(parent, x)
            y_root = find(parent, y)

            if rank[x_root] < rank[y_root]:
                parent[x_root] = y_root
            elif rank[x_root] > rank[y_root]:
                parent[y_root] = x_root
            else:
                parent[y_root] = x_root
                rank[x_root] += 1

        result = []
        parent, rank = [], []
        node_name = {i: x for i, x in enumerate(self.get_nodes())}

        for id in range(self.V()):
            parent.append(id)
            rank.append(0)

        e_cnt = 0
        for (cost, v, w) in self.get_edges():
            if e_cnt == (self.V() - 1):
                break
            x = find(parent, v)
            y = find(parent, w)
            if x != y:
                e_cnt += 1
                result.append([node_name[v], node_name[w], cost])
                union(parent, rank, x, y)

        for v, w, cost in result:
            print("%s -- %s == %d" % (v, w, cost))


def main(G, input_file):
    """Read file and load graph info"""
    for line in open(input_file, 'r'):
        line = line.rstrip('\n').replace(', ', ',').split(',')
        [v, w, cost] = line[0], line[1], int(line[2])
        G.add_edge(v, w, cost)


if __name__ == '__main__':

    G = Graph()  # construct a graph instance G
    INPUT_FILE = "graph.txt"
    main(G, INPUT_FILE)  # read graph.txt into G
    print("number of vertices: %s" % G.V())
    print("number of edges: %s" % G.E())
    # print G.get_edges()
    # G.mst()
