import math
import random
from utils import Stack, Queue, PriorityQueue, Node, cal_path_cost
from quicksort.quicksort import quicksort

"""Calculate heuristic for astar"""

def astar_heuristic(problem, child_node):
    """Calculate heuristic for astar"""
    def distance(v, w):
        (x1, y1, z1) = problem['coords'][v]
        (x2, y2, z2) = problem['coords'][w]
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)

    if problem['domain'] == 'route':
        return distance(child_node.value, problem['goal'])

    elif problem['domain'] == 'tsp':
        path = child_node.get_path()
        visited_set = set(path)
        heuristic = 0
        for node_value in problem['graph'].get_nodes():
            if node_value not in visited_set:  # nonvisited node
                heuristic += distance(child_node.value, node_value)
        return heuristic
    print("wrong domain")
    return False


def goal_test(problem, node):
    if problem['domain'] == 'route':
        return node.value == problem['goal']
    elif problem['domain'] == 'tsp':  # no need to return initial city
        path = node.get_path()
        visited_set = set(path)
        return len(visited_set) == len(problem['graph'].get_nodes())
    print("wrong domain")
    return False


def push_or_not(problem, node, child_value, closed_set):
    """route planning: use graph search to avoid repeat nodes,
        but be careful to Astar (still need to check cost)
    tsp: tree search
    """
    if problem['domain'] == 'route' and problem['method'] == 'A': #Todo: Astar not optimal, use tree
        return child_value not in closed_set
    elif problem['domain'] == 'route':  # if the city has been expanded before, dont push to queue
        return child_value not in closed_set

    elif problem['domain'] == 'tsp':
        if problem['method'] in ['B', 'I', 'U', 'A']:
            return True
        elif problem['method'] == 'D':  # loop problem: use random select
            if node.depth <= 2:  # ensure enough nodes are in the stack
                return True
            return random.randint(0, 1)


def general_search(problem):
    """Problem: {doamin, method, graph, coords, start, goal}
    method: B, D, I, U, A

    route: graph search (maintain a closed set) except Astar
    tsp: tree search
    """
    method = problem['method']

    if method not in ['B', 'D', 'I', 'U', 'A']:
        print("Enter Correct method!")
        return None
    if problem['start'] not in problem['graph'].get_nodes() or (
            problem['domain'] == 'route' and problem['goal'] not in problem['graph'].get_nodes()):
        print("Enter Correct Start/Goal!")
        return None

    # BFS, DFS
    if method in ['B', 'D']:
        if method == 'B':
            frontier = Queue()
        else:
            frontier = Stack()
        start_node = Node(problem['start'])
        frontier.push(start_node)
        closed_set = set()
        while not frontier.isEmpty():
            node = frontier.pop()
            closed_set.add(node.value)
            if goal_test(problem, node):
                path = node.get_path()
                cost = cal_path_cost(problem['graph'], path)
                return path, cost, frontier.count

            # Expansion
            closed_set.add(node.value)
            adj = problem['graph'].adj(node.value)
            for child_value in quicksort(adj):
                if push_or_not(problem, node, child_value, closed_set):
                    child_node = Node(child_value, node)
                    frontier.push(child_node)
        return None

    """Uniform Cost Search / Astar Search"""
    if method in ['U', 'A']:
        frontier = PriorityQueue()
        start_node = Node(problem['start'])
        priority = 0 if method == 'U' else astar_heuristic(problem, start_node)
        frontier.push(priority, start_node)

        closed_set = set()

        while not frontier.isEmpty():
            node = frontier.pop()
            closed_set.add(node.value)
            if goal_test(problem, node):
                path = node.get_path()
                cost = cal_path_cost(problem['graph'], path)
                return path, cost, frontier.count
            # Expansion
            adj = problem['graph'].adj(node.value)
            for child_value in quicksort(adj):
                if push_or_not(problem, node, child_value, closed_set):
                    child_cost = node.cost_so_far + \
                        problem['graph'].get_cost(node.value, child_value)  # g_n
                    child_node = Node(child_value, node, child_cost)
                    priority = child_cost if method == 'U' else child_cost + \
                        astar_heuristic(problem, child_node)
                    frontier.push(priority, child_node)
        return None

    """Iterative Deepening Search"""
    if method == 'I':
        def depth_limited(problem, limit):
            """Depth Limited Search"""
            frontier = Stack()
            start_node = Node(problem['start'])
            frontier.push(start_node)
            closed_set = set()
            while not frontier.isEmpty():
                node = frontier.pop()
                closed_set.add(node.value)
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
                            child_node = Node(child_value, node)
                            frontier.push(child_node)
            return None
        max_depth = 20
        for i in range(max_depth):
            result = depth_limited(problem, i)
            if result:
                return result
