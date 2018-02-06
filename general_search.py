from quicksort.quicksort import quicksort
from utils import Stack, Queue, PriorityQueue, cal_path_cost, Node
import math
import random

def astar_heuristic(problem,child_value):
    if problem['domain'] == 'route':
        v, w = child_value, problem['goal']
        (x1, y1, z1) = problem['coords'][v]
        (x2, y2, z2) = problem['coords'][w]
        return math.sqrt( (x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2 )

def goal_test(problem, node):
    if problem['domain'] == 'route':
        return node.value == problem['goal']
    elif problem['domain'] == 'tsp': # no need to return initial city
        path = node.get_path()
        visited_set = set(path)
        return len(visited_set) == len(problem['graph'].get_nodes())

def push_or_not(problem,node,child_value,closed_set):
    if problem['domain'] == 'route': # if the city has been expanded before, dont push to the queue
        return child_value not in closed_set

    elif problem['domain'] == 'tsp':
        if problem['method'] in ['B','I','U']:
            return True
        elif problem['method'] == 'D': # loop problem: use random select
            if node.depth <= 2: # ensure enough nodes are in the stack
                return True
            return random.randint(0, 1)
        elif problem['method'] == 'A': # heuristic
            return
            # return not node.parent or (node.parent and child_value != node.parent.value)

def general_search(problem):
    """Problem: {graph:, coords:, start:, goal:}
    method: B, D, I, U, A

    route: graph search (maintain a closed set)
    tsp: tree search
    """
    method = problem['method']

    if method not in ['B', 'D', 'I', 'U', 'A']:
        print ("Enter Correct method!")
        return None
    if problem['start'] not in problem['graph'].get_nodes() or (problem['domain'] == 'route' and problem['goal'] not in problem['graph'].get_nodes()):
        print("Enter Correct Start/Goal!")
        return None

    # BFS, DFS
    if method in ['B','D']:
        if method == 'B':
            frontier = Queue()
        else:
            frontier = Stack()
        frontier.push( Node(problem['start']) )
        closed_set = set()
        while not frontier.isEmpty():
            node = frontier.pop()
            closed_set.add(node.value)
            print ("node: %s" % node)
            if goal_test(problem, node):
                path = node.get_path()
                cost = cal_path_cost(problem['graph'],path)
                return path, cost, frontier.count

            # Expansion
            closed_set.add(node.value)
            adj = problem['graph'].adj(node.value)
            for child_value in quicksort(adj):
                if push_or_not(problem, node, child_value, closed_set):
                # if child_value not in closed_set: # route
                # if True:  # tsp: BFS
                # if random.randint(0, 1):  # tsp: DFS
                    child = Node(child_value, node)
                    frontier.push(child)
                    print "->push", child
            # print frontier
            print("------------------------------")
        return None

    # UCS, Astar
    if method in ['U','A']:
        frontier = PriorityQueue()
        priority = 0 if method == 'U' else astar_heuristic(problem, problem['start'])
        frontier.push(priority, Node(problem['start']))

        closed_set = set()
        cost = dict()
        cost[problem['start']] = 0

        while not frontier.isEmpty():
            node = frontier.pop()
            closed_set.add(node.value)
            print "node:", node, node.cost_so_far
            if goal_test(problem, node):
                path = node.get_path()
                cost = cal_path_cost(problem['graph'],path)
                return path, cost, frontier.count
            # Expansion
            adj = problem['graph'].adj(node.value)
            for child_value in quicksort(adj):
                if push_or_not(problem, node, child_value, closed_set):
                # if not node.parent or (node.parent and child_value != node.parent.value): # tsp
                # if child_value not in closed_set:  # route
                    child_cost = node.cost_so_far + problem['graph'].get_cost(node.value, child_value)  # g_n
                    priority = child_cost if method == 'U' else child_cost + astar_heuristic(problem, child_value)
                    child = Node(child_value, node, child_cost)
                    frontier.push(priority,child)
                    print "->push", child, child_cost
            # print frontier
            print("------------------------------")
        return None

    # IDS
    if method == 'I':
        def depth_limited(problem, limit):
            frontier = Stack()
            frontier.push(Node(problem['start']))
            closed_set = set()
            while not frontier.isEmpty():
                node = frontier.pop()
                closed_set.add(node.value)
                print "node:", node
                if goal_test(problem, node):
                    path = node.get_path()
                    cost = cal_path_cost(problem['graph'], path)
                    return path, cost, frontier.count
                if node.depth == limit:
                    pass
                else:
                    # Expansion
                    adj = problem['graph'].adj(node.value)
                    for child_value in quicksort(adj):
                        if push_or_not(problem, node, child_value, closed_set):
                        # if child_value not in closed_set: # route
                        # if True:  # tsp
                            child = Node(child_value, node)
                            frontier.push(child)
                            print "->push", child
                # print frontier
                print("------------------------------")
            return None
        max_depth = 20
        for i in range(max_depth):
            result = depth_limited(problem, i)
            if result:
                return result