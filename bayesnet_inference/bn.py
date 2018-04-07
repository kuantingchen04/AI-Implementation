#!/usr/bin/env python


"""Enumerate by Interence Implementation (enumerate-ask, enumerate-all)"""

import copy
import itertools

class BayesNet:
    """Bayes Net Implementation, maintaining a network dict and union-find's id"""

    def __init__(self):
        self.bn = dict()
        self._id = []  # for uf
        self._sz = []  # for uf

    def add_var(self, var):
        """For each var: record its parent/child/prob"""
        self.bn[var] = {'parents': [], 'cond_prob': {}, 'childs': []}

    def add_edge(self, u, v):
        """
        1. Update child/parent
        2. Update union-find
        """

        self.bn[v]['parents'].append(u)
        self.bn[u]['childs'].append(v)

        all_vars = self.all_vars()
        self.uf_union(all_vars.index(u), all_vars.index(v))

    def add_prob(self, node, cond_nodes, prob):
        """
        Update the probability of var
            input: D=T, ['B=T', 'C=T'], 0.1
        """

        node, node_val = node.split("=")

        if node_val == 'F':
            prob = 1.0 - float(prob)
        else:
            prob = float(prob)

        if not cond_nodes:
            self.bn[node]['cond_prob'][None] = prob
        else:
            bag = {x.split('=')[0]: x.split('=')[1]
                   for x in cond_nodes}  # { B:T, C:T }
            pairs = [bag[pa] for pa in self.bn[node]
                     ['parents']]  # [T,T] in parents order
            pairs = [True if x == 'T' else False for x in pairs]  # [1,1]
            self.bn[node]['cond_prob'][tuple(pairs)] = prob

    def uf_init(self):
        """Initialize the union-find algo (after getting num of var)"""
        n = len(self.bn.keys())
        self._id = list(range(n))
        self._sz = [1] * n

    def uf_root(self, i):
        """Retrieve the root"""
        j = i
        while j != self._id[j]:
            self._id[j] = self._id[self._id[j]]
            j = self._id[j]
        return j

    def uf_find(self, p, q):
        """Check if two elements are in the same component"""
        return self.uf_root(p) == self.uf_root(q)

    def uf_union(self, p, q):
        """Add the edge, do the union"""
        i = self.uf_root(p)
        j = self.uf_root(q)
        if i == j:
            return
        if self._sz[i] < self._sz[j]:
            self._id[i] = j
            self._sz[j] += self._sz[i]
        else:
            self._id[j] = i
            self._sz[i] += self._sz[j]

    def all_vars(self):
        """Return all var in Bayes Net"""
        return self.bn.keys()

    def same_component_vars(self, q_var):
        """Given a var, we only return vars which are in same graph (using union-find)"""
        res = []
        idx_q = self.bn.keys().index(q_var)
        for i, x in enumerate(self.bn.keys()):
            if self.uf_find(self._id[i], self._id[idx_q]):
                res.append(x)
        return res

    def reduce_e(self, q_var, e_vars):
        """If the evidence include vars in other components, then we remove it"""
        res_e = dict()
        for k, v in e_vars.iteritems():
            if k in self.same_component_vars(q_var):
                res_e[k] = v
        return res_e

    def get_toposort(self, _vars=None):
        """All parents of a node has to be added before the node is added"""
        if not _vars:
            _vars = self.bn.keys()

        _vars = copy.copy(_vars)

        goal = len(_vars)
        res = []
        visit = set()

        def topo_helper(var):
            """Helper function for topological sort"""
            # invalid
            if len(res) == goal:
                return

            # Success or not
            visit.add(var)

            childs = self.bn[var]['childs']
            for child in childs:
                if child in visit:
                    continue
                else:
                    topo_helper(child)
            res.append(var)

        while len(res) != goal:
            unvisit_vars = [x for x in _vars if x not in res]
            topo_helper(unvisit_vars[-1])
        return res

    def __str__(self):
        return str(self.bn)


# Parsers
def read_bn(fname):
    """Update vars -> Arc -> Prob"""

    BN = BayesNet()

    with open(fname, 'r') as f:

        f.readline()  # skip first line

        # RV
        s = f.readline()
        _vars = s.replace(' ', '').rstrip('\n').split(',')
        for var in _vars:
            BN.add_var(var)
        BN.uf_init()

        # Arc
        f.readline()  # skip
        while True:
            s = f.readline()
            if '%' in s:
                break
            u, v = s.replace(' ', '').rstrip('\n').split(',')
            BN.add_edge(u, v)

        # Prob
        # P(D=T|B=T,C=T)=0.1 -> ['D=T', 'B=T', 'C=T', '0.1'] -> D:{(T,T):0.1}
        # P(A=T)=0.4 -> ['A=T', '0.4'] -> A:{None:0.4}
        while True:
            s = f.readline()
            if s == '':  # eof
                break
            s = s.rstrip('\n').replace(
                'P(', '').replace(')=', '|').replace(',', '|').split('|')
            node, cond_nodes, prob = s[0], s[1:-1], s[-1]
            BN.add_prob(node, cond_nodes, prob)
    return BN


def read_input(fname):
    """Get query and evidence"""
    with open(fname, 'r') as f:
        f.readline()  # skip

        # Qeury
        q = f.readline().rstrip('\n')
        f.readline()  # skip

        # Evidence
        e = {}
        s = f.readline()
        if s != '\n':  # if evidence provided
            s = s.rstrip('\n').replace(' ', '').split(',')  # ['A=T', 'C=F']
            e = {x.split('=')[0]: True if x[-1] == 'T' else False for x in s}
    return q, e


# Program
def enumerate_inference(q_var, e_vars, BN):
    """Handle disconnet component & Handle zero case"""
    # Reduce E to same component
    e_vars = BN.reduce_e(q_var, e_vars)

    # Zero
    combo = list(itertools.product([1, 0], repeat=len(e_vars)))
    lst = e_vars.keys()
    res = [0, 0]
    for com in combo:
        try_e = {}
        for i, x in enumerate(com):
            if x:
                try_e[lst[i]] = e_vars[lst[i]]
        log(try_e)
        res = enumerate_ask(q_var, try_e, BN)
        if sum(res) != 0:
            return res
    return res


def enumerate_ask(q_var, e_vars, BN):
    """Goal: P(Q|e1,e2,e3...)"""
    res = []  # P(Q)
    for xi in [True, False]:
        _vars = BN.get_toposort(BN.same_component_vars(q_var))
        new_e = copy.copy(e_vars)
        new_e[q_var] = xi
        res.append(enumerate_all(_vars, new_e, BN))

    return normalize(res)


def enumerate_all(_vars, e_vars, BN):
    """Recursion helper"""
    if not _vars:
        return 1.0

    _vars = copy.copy(_vars)
    var = _vars.pop()

    if var in e_vars:
        e_1 = copy.copy(e_vars)
        return pr(var, e_1, BN) * enumerate_all(_vars, e_1, BN)
    e_t = copy.copy(e_vars)
    e_t[var] = True

    e_f = copy.copy(e_vars)
    e_f[var] = False
    return pr(var, e_t, BN) * enumerate_all(_vars, e_t, BN) + \
        pr(var, e_f, BN) * enumerate_all(_vars, e_f, BN)


def pr(var, e, BN):
    """Computer the probability"""
    # log(var, E)
    pa = BN.bn[var]['parents']
    if not pa:  # no parents -> return margin
        prob = BN.bn[var]['cond_prob'][None]
    else:
        key = tuple([e[x] for x in pa])
        prob = BN.bn[var]['cond_prob'][key]

    if not e[var]:
        prob = 1.0 - prob

    # print (E, var, pa, prob)
    return prob


# Utils
def normalize(vec):
    """Normalize the dist if not 0"""
    if sum(vec) != 0:
        return tuple(x / sum(vec) for x in vec)
    return vec


def log(*args):
    """For Debugging"""
    # print(args)
    pass


def main():
    """Read Bayes Net and Input, computer the prob. dist."""
    BN = read_bn("tests/bn.txt")
    query, evidence = read_input("tests/input.txt")

    res = enumerate_inference(query, evidence, BN) # main program
    print("%.3f %.3f" % (res[0], res[1]))


if __name__ == '__main__':
    main()
