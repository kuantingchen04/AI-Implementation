- Code
    - mysearch.py: The top-level function to specify domain/methods. It also read the Southern Michigan data for constructing the graph
    - general_search.py: Main code for various search methods. (B, D, I, U, A)
    - quicksort.py: From hw1
    - mygraph.py: From hw1
    - utils.py: Several classes implementation

- Inputs
    - route.txt: Input of route planning problem
    - tsp.txt: Input of tsp problem
    - data/transition.csv: Graph edges (u,v,weight)
    - data/latlon.csv: Info of cities (lat,lon)


- Instruction:
    At bottom of "mysearch.py", the code is as followed:

        if __name__ == '__main__':

            domain = "tsp" # route/tsp
            path_set = {
                "GRAPH_FILE": "data/transition.csv",
                "COORDS_FILE": "data/latlon.csv",
                "DOMAIN_ROUTE_FILE": "route.txt",
                "DOMAIN_TSP_FILE": "tsp.txt"
            }
            main(domain, path_set)

    1. Simply assign the domain to "route" or "tsp"
    2. The program will read the domain info and method specified in "route.txt" / "tsp.txt"
       It will also read the graph info in data/ directory
       However, you could change the path manually (change path_set dictionary)
    3. Run "python mysearch.py", then the results will be printed out


- Overview for general search code
    Though there are five methods and two domains, the implementation is very similar.
    The main difference of route planing and TSP is:
        1. goal_test:
            For route planning problem, it checks if current node is the goal
            For TSP, it checks if all cities have been visited

        2. push to queue or not:
            For route planning problem, it maintains a closed set to avoid expanding the same city
            For TSP, since same city may occur on the path, it explores all possible children
            * For DFS in TSP, in order to avoid loops, we randomly decide whether pushing the children to the queue (Mentioned by Professor)

    - Five methods are implemented
        - Breadth-first Search / Depth-first Search: The difference is BFS uses queue and DFS uses stack
        - Uniform Cost Search / Astar Search: Astar uses heuristic (from the lat/lon), but USC doesn't
        - Iterative Deepening Search: Iteratively call a Depth Limited Search to check if search is successful

- Heuristic in TSP
    Since the goal of TSP is to check if all cities have been visited at least once,
        we could use the distance to travel all the unvisited cities as the Heuristic.

    To estimate the distance, we could use a summation of the straight line distance using the lat/lon info.
    We could also construct a minimum spanning tree to guarantee the heuristic is admissible