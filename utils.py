# class Node:



class Stack:
    def __init__(self):
        self.items = []
        self.count = 0

    def isEmpty(self):
        return self.items == []

    def push(self,item):
        self.items.append(item)

    def pop(self):
        self.count += 1
        return self.items.pop()

    def size(self):
        return len(self.items)

    def __contains__(self, item):
        return item in self.items

class Queue:
    def __init__(self):
        self.items = []
        self.count = 0

    def isEmpty(self):
        return self.items == []

    def push(self,item):
        self.items.append(item)

    def pop(self):
        self.count += 1
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
        self.count = 0

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
        self.count += 1
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

if __name__ == '__main__':
    PQ = PriorityQueue()
    PQ.push(5,'A')
    PQ.push(5,'A')
    PQ.push(5,'B')
    PQ.push(2,'C')

    print PQ.items
    print PQ.pop()
    print PQ.items