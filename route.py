from quicksort.quicksort import quicksort
from utils import Stack, Queue, PriorityQueue, trace_back, cal_path_cost
import math

def heuristic(coords,v,w):
    (x1, y1, z1) = coords[v]
    (x2, y2, z2) = coords[w]
    return math.sqrt( (x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2 )

def graph_search(problem, strategy):
    """Problem: {graph:, coords:, start:, goal:}
    Strategy: B, D, I, U, A
    """
    if strategy not in ['B', 'D', 'I', 'U', 'A']:
        print ("Enter Correct Strategy!")
        return None
    if problem['start'] not in problem['graph'].get_nodes() or problem['goal'] not in problem['graph'].get_nodes():
        print("Enter Correct Start/Goal!")
        return None

    # BFS, DFS
    if strategy in ['B','D']:
        if strategy == 'B':
            frontier = Queue()
        else:
            frontier = Stack()
        frontier.push(problem['start'])
        closed_set = set()
        node_to = { x: None for x in problem['graph'].get_nodes()}

        while not frontier.isEmpty():
            node = frontier.pop()
            print "node:",node
            if node == problem['goal']:
                path = trace_back(node_to,problem['goal'])
                cost = cal_path_cost(problem['graph'],path)
                return path, cost, frontier.count
            # Expansion
            closed_set.add(node)
            print "expand", node
            adj = problem['graph'].adj(node)
            quicksort(adj)
            print "child:", adj
            for child in adj:
                if child not in closed_set and child not in frontier: # dont allow duplicates in frontier
                    frontier.push(child)
                    print "push", child
                    node_to[child] = node
            print "queue:", frontier.items
        return None

    # UCS, Astar
    if strategy in ['U','A']:
        frontier = PriorityQueue()
        priority = 0 if strategy == 'U' else heuristic(problem['coords'],problem['goal'],problem['start'])
        frontier.push(priority, problem['start'])

        closed_set = set()
        node_to = {x: None for x in problem['graph'].get_nodes()}
        cost = dict()
        cost[problem['start']] = 0

        while not frontier.isEmpty():
            node = frontier.pop()
            if node == problem['goal']:
                path = trace_back(node_to,problem['goal'])
                cost = cal_path_cost(problem['graph'],path)
                return path, cost, frontier.count
            # Expansion
            closed_set.add(node)
            print "expand", node
            adj = problem['graph'].adj(node)
            quicksort(adj)
            print "child:", adj
            for child in adj:
                new_cost = cost[node] + problem['graph'].get_cost(node,child) # g_n

                if child not in cost or new_cost < cost[child]:
                    del frontier[child] # if key with lower priority is in frontier, delete it first
                    cost[child] = new_cost
                    priority = new_cost if strategy == 'U' else new_cost + heuristic(problem['coords'],problem['goal'],child)
                    frontier.push(priority,child)
                    node_to[child] = node
                    print "push", child

            print "queue:", frontier.items
        return None

    # IDS
    if strategy == 'I':
        def DLS(problem, limit):

            path = []
            def rec_dls(node, problem, limit):
                if problem['goal'] == node:
                    path.append(node)
                    return node
                elif limit <= 0:
                    return "cutoff"
                else:
                    cutoff_occured = False
                    # Expansion
                    adj = problem['graph'].adj(node)
                    quicksort(adj)
                    for child in adj[::-1]:
                        result = rec_dls(child, problem, limit - 1)
                        if result == 'cutoff':
                            cutoff_occurred = True
                        elif result is not None:
                            path.append(node)
                            return result
                    return 'cutoff' if cutoff_occurred else None

            return rec_dls(problem['start'], problem, limit), path[::-1]

        max_depth = 15
        for i in range(max_depth):
            count = 0
            result, path = DLS(problem, i)
            if result != 'cutoff':
                cost = cal_path_cost(problem['graph'], path)
                return  path, cost, count