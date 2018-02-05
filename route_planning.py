from quicksort.quicksort import quicksort
import math

def trace_back(node_to, goal):
    path = []
    while goal != None:
        path.insert(0,goal)
        goal = node_to[goal]
    return path

def cal_path_cost(graph,path):
    cost = 0
    if len(path) > 1:
        i = 0
        while i < (len(path) - 1):
            cost += graph.get_cost(path[i],path[i+1])
            i += 1
    return cost

def heuristic(coords,v,w):
    (x1, y1, z1) = coords[v]
    (x2, y2, z2) = coords[w]
    print v,w,math.sqrt( (x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2 )
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
                return path, cost, closed_set
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
                return path, cost, closed_set
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
            closed_set = set()

            def rec_dls(node, problem, limit):
                if problem['goal'] == node:
                    path.append(node)
                    return node
                elif limit <= 0:
                    return "cutoff"
                else:
                    cutoff_occured = False
                    # Expansion
                    closed_set.add(node)
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

            return rec_dls(problem['start'], problem, limit), path[::-1], closed_set

        max_depth = 15
        for i in range(max_depth):
            result, path, closed_set = DLS(problem, i)
            if result != 'cutoff':
                cost = cal_path_cost(problem['graph'], path)
                return  path, cost, closed_set


class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self,item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

    def __contains__(self, item):
        return item in self.items

class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self,item):
        self.items.append(item)

    def pop(self):
        return self.items.pop(0)

    def size(self):
        return len(self.items)

    def __contains__(self, item):
        return item in self.items

class PriorityQueue:
    """
    storing tuples in PQ: (priority, item)
    order: return the min/max item first
    """
    def __init__(self, order=min):
        self.items = []
        self.order = order

    def isEmpty(self):
        return self.items == []

    def push(self, priority, item):
        """insert items in order"""
        # self.item.append(item)
        x = (priority, item)

        if not self.items:
            self.items.append(x)
            return

        lo, hi = 0, len(self.items)
        while lo < hi:
            mid = (lo+hi) // 2
            if x > self.items[mid]:
                lo = mid + 1
            else:
                hi = mid
        self.items.insert(lo, x)

    def pop(self):
        if self.order == min:
            return self.items.pop(0)[1]
        else:
            return self.items.pop()[1]

    def size(self):
        return len(self.items)

    def __contains__(self, item):
        keys = [ key for (priority,key) in self.items]
        return item in keys

    def __delitem__(self, item):
        for i, (priority,key) in enumerate(self.items):
            if item == key:
                self.items.pop(i)

if __name__ == '__main__':
    PQ = PriorityQueue()
    PQ.push(5,'A')
    PQ.push(5,'A')
    PQ.push(5,'B')
    PQ.push(2,'C')

    print PQ.items
    print PQ.pop()
    print PQ.items