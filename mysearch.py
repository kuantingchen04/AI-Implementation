import argparse
import csv
import math
from graph.mygraph import Graph

def parse_args():
    """Parse input arguments."""
    parser = argparse.ArgumentParser(description='Route Planning')
    parser.add_argument('--origin', dest='start', help='Origin Location',
                        default='Ann Arbor', type=str, required=False)
    parser.add_argument('--destination', dest='goal', help='Destination Location',
                        default='Detroit', type=str, required=False)
    parser.add_argument('--algo', dest='algo', help='Search algorithm choice (B, D, I, U, A)',
                        default='A', type=str)
    args = parser.parse_args()
    return args

def read_graph(G, input_file):
    with open(input_file, 'r') as f:
        csv_reader = csv.reader(f)
        for line in csv_reader:
            [v, w, cost] = line[0], line[1], float(line[2])
            G.add_edge(v, w, cost)

def get_coords(input_file):
    coords = {}
    with open(input_file, 'r') as f:
        csv_reader = csv.reader(f)
        for line in csv_reader:
            [loc_name, lat, lon] = line[0], float(line[1]), float(line[2])
            coords[loc_name] = latlon_to_cartesian(lat, lon)
    return coords

def latlon_to_cartesian(lat,lon):
    R = 3959
    phi = (lat * math.pi) / 180
    theta = (lon * math.pi) / 180
    x = math.cos(phi) * math.cos(theta) * R
    y = math.cos(phi) * math.sin(theta) * R
    z = math.sin(phi)
    return (x,y,z)

def main(domain):
    # Read graph info from csv files
    G = Graph()
    read_graph(G, "data/transition.csv")
    coords = get_coords("data/latlon.csv")

    if domain == "route":
        # Q2: Get domain and search method from route.txt
        from route import graph_search
        route_info = []
        for line in open("route.txt"):
            route_info.append(line.strip('\n'))
        start, goal, method = route_info[:3]
        problem = {'graph': G, 'coords': coords, 'start': start, 'goal': goal}

    elif domain == "tsp":
        # Q3: Get domain and search method from tsp.txt
        from tsp import graph_search
        tsp_info = []
        for line in open("tsp.txt"):
            tsp_info.append(line.strip('\n'))
        start, method = tsp_info[:2]
        problem = {'graph': G, 'coords': coords, 'start': start, 'goal': start}

    result = graph_search(problem, method) # my search algorithm
    if result:
        path, cost, count = result

        print("------------------------------")
        print("nodes expanded: \t %s" % count)
        print("solution path: \t %s" % " -> ".join(path))
        print("total cost: \t %s" % cost)
    else:
        print("Search failed!")

if __name__ == '__main__':

    domain = "route" # route/tsp
    main(domain)







