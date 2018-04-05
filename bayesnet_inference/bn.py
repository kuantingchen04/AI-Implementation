#!/usr/bin/env python

import copy
import itertools

class BayesNet:
    def __init__(self):
        self.bn = dict()

    def add_var(self, var):
        self.bn[var] = { 'parents': [],'cond_prob': {}, 'childs': [] }

    def add_edge(self, u, v):
        """from u to v"""
        self.bn[v]['parents'].append(u)
        self.bn[u]['childs'].append(v)

    def add_prob(self, node, cond_nodes, prob):
        # D=T, ['B=T', 'C=T'], 0.1
        # print node
        node, node_val = node.split("=")

        if node_val=='F':
            prob = 1.0 - float(prob)
        else:
            prob = float(prob)

        if not cond_nodes:
            self.bn[node]['cond_prob'][None] = prob
        else:
            bag = { x.split('=')[0]:x.split('=')[1] for x in cond_nodes } # { B:T, C:T }
            pairs = [ bag[pa] for pa in self.bn[node]['parents']] # [T,T] in parents order
            pairs = [True if x=='T' else False for x in pairs] # [1,1]
            self.bn[node]['cond_prob'][tuple(pairs)] = prob

    def get_order_vars(self):
        """Return vars respect to # of parents (small->big)"""
        vars = self.bn.keys()
        vars_pa = [ len(self.bn[x]['parents']) for x in vars ]
        sort_vars = [ x for _,x in sorted(zip(vars_pa,vars))]
        return sort_vars

    def get_var_toposort(self, vars=None):
        if not vars:
            vars = self.bn.keys()

        vars = copy.copy(vars)

        goal = len(vars)
        res = []
        visit = set()

        def topo_helper(var):

            # invalid
            if len(res) == goal: #invalid
                # return res[::-1]
                return

            # success or not
            visit.add(var)

            childs = self.bn[var]['childs']
            for child in childs:
                if child in visit:
                    continue
                else:
                    topo_helper(child)
            res.append(var)

        while len(res) != goal:
            unvisit_vars = [ x for x in vars if x not in res ]
            topo_helper(unvisit_vars[-1])

        return res

    def __str__(self):
        return str(self.bn)

## Parser
def read_bn(fname):

    # BN
    BN = BayesNet()

    # RV -> Arc -> Prob
    with open(fname, 'r') as f:

        f.readline() # skip first line

        # RV
        s = f.readline()
        vars = s.replace(' ','').rstrip('\n').split(',')
        for var in vars:
            BN.add_var(var)

        # Arc
        f.readline() # skip
        while True:
            s = f.readline()
            if '%' in s:
                break
            u,v = s.replace(' ', '').rstrip('\n').split(',')
            BN.add_edge(u,v)

        # Prob
        # P(D=T|B=T,C=T)=0.1 -> ['D=T', 'B=T', 'C=T', '0.1'] -> D:{(T,T):0.1}
        # P(A=T)=0.4 -> ['A=T', '0.4'] -> A:{None:0.4}
        while True:
            s = f.readline()
            if s == '': # eof
                break
            s = s.rstrip('\n').replace('P(','').replace(')=','|').replace(',','|').split('|')
            node, cond_nodes, prob = s[0], s[1:-1] ,s[-1]
            BN.add_prob(node, cond_nodes, prob)
    return BN

def read_input(fname):
    """Get query and evidence"""
    with open(fname, 'r') as f:
        f.readline()  # skip

        # Qeury
        Q = f.readline().rstrip('\n')
        f.readline()  # skip

        # Evidence
        E = {}
        s = f.readline()
        if s != '\n': # if evidence provided
            s = s.rstrip('\n').replace(' ','').split(',') # ['A=T', 'C=F']
            E = { x.split('=')[0]:True if x[-1]=='T' else False for x in s }
    return Q, E


# Program
# here copy is fine
def enumerate_inference(Q, E, BN):
    """Handle zero case"""
    combo = list(itertools.product([1, 0], repeat=len(E)))
    lst = E.keys()
    for com in combo:
        new_E = {}
        for i,x in enumerate(com):
            if x:
                new_E[lst[i]] = E[lst[i]]
        log(new_E)
        res = enumerate_ask(Q, new_E, BN)
        if sum(res) != 0:
            return res


def enumerate_ask(Q, E, BN):
    """Goal: P(Q|e1,e2,e3...)"""
    res = [] # P(Q)
    for xi in [True, False]:
        vars = BN.get_var_toposort()
        extend_E = copy.copy(E)
        extend_E[Q] = xi
        res.append(enumerate_all(vars, extend_E, BN))

    return normalize(res)
cnt = 0
def enumerate_all(vars, E, BN):
    global cnt
    cnt += 1
    if not vars:
        return 1.0

    vars = copy.copy(vars)
    var = vars.pop()

    if var in E:
        E1 = copy.copy(E)
        return Pr(var, E1, BN) * enumerate_all(vars, E1, BN)
    else:
        ET = copy.copy(E)
        ET[var] = True

        EF = copy.copy(E)
        EF[var] = False
        return Pr(var, ET, BN) * enumerate_all(vars, ET, BN) + Pr(var, EF, BN) * enumerate_all(vars, EF, BN)


def Pr(var, E, BN):
    # log(var, E)
    pa = BN.bn[var]['parents']
    if len(pa)==0: # no parents -> return margin
        prob = BN.bn[var]['cond_prob'][None]
    else:
        key = tuple([ E[x] for x in pa])
        prob = BN.bn[var]['cond_prob'][key]


    if E[var] != True:
        prob = 1.0-prob

    # print (E, var, pa, prob)
    return prob

# Utils
def normalize(vec):
    if sum(vec)!=0:
        return tuple(x / sum(vec) for x in vec)
    return vec

def log(*args):
    print (args)
    pass

def main():

    BN = read_bn("tests/bn.txt")
    # print (BN)

    Q,E = read_input("tests/input.txt")

    res = enumerate_inference(Q,E,BN)
    print "%.3f %.3f" % (res[0],res[1])
    log(cnt)

if __name__ == '__main__':
    main()


