from quicksort.quicksort import quicksort
from utils import Stack, Queue, PriorityQueue, trace_back, cal_path_cost

def graph_search(problem, strategy):
    """Problem: {graph:, coords:, start:, goal:}
    Strategy: B, D, I, U, A
    """
    if strategy not in ['B', 'D', 'I', 'U', 'A']:
        print ("Enter Correct Strategy!")
        return None
    if problem['start'] not in problem['graph'].get_nodes() or problem['goal'] not in problem['graph'].get_nodes():
        print("Enter Correct Start!")
        return None

    if strategy == 'D':
        frontier = Stack()
        frontier.push(problem['start'])
        prev_node = None
        prev_prev_node = None
        closed_set = set()
        # node_to = { x: None for x in problem['graph'].get_nodes()}

        i = 0
        while not frontier.isEmpty():
            node = frontier.pop()
            print "node:",node

            # goal test
            if node == problem['goal'] and len(closed_set) == len(problem['graph'].get_nodes()):
                print "Get"
                return
                # path = trace_back(node_to,problem['goal'])
                # cost = cal_path_cost(problem['graph'],path)
                # return path, cost, closed_set
            # Expansion
            closed_set.add(node)
            # print "expand", node
            adj = problem['graph'].adj(node)
            quicksort(adj)
            print "child:", adj
            for child in adj:
                if child == prev_node or child == prev_prev_node: # prevent cycle
                    print "Cycle"
                    continue
                # if child not in closed_set and child not in frontier: # dont allow duplicates in frontier
                frontier.push(child)
                print "push", child
                # node_to[child] = node
            prev_prev_node = prev_node
            prev_node = node
            print closed_set, prev_node, prev_prev_node
            print "queue:", frontier.items
            if i == 15:
                break
            i += 1

        return None

    if strategy == 'U':
        frontier = PriorityQueue()
        priority = 0
        frontier.push(priority, problem['start'])

        closed_set = set()
        node_to = {x: None for x in problem['graph'].get_nodes()}
        cost = dict()
        cost[problem['start']] = 0
        cnt = 0
        path = []

        while not frontier.isEmpty():
            node = frontier.pop()
            path.append(node)
            # if node == problem['goal']:
            if len(closed_set) == len(problem['graph'].get_nodes()):
                path = trace_back(node_to,problem['goal'])
                cost = cal_path_cost(problem['graph'],path)
                return path, cost, closed_set
            # Expansion
            cnt += 1
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
                    priority = new_cost
                    frontier.push(priority,child)
                    node_to[child] = node
                    print "push", child

            print "queue:", frontier.items
            print closed_set, len(problem['graph'].get_nodes()), cnt
        print path
        return None