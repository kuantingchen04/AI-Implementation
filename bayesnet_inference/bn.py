#!/usr/bin/env python

class BayesNet:
    def __init__(self):
        self.bn = dict()

    def add_var(self, var):
        self.bn[var] = { 'parents': [],'cond_prob': {} }

    def add_edge(self, u, v):
        """from u to v"""
        self.bn[v]['parents'].append(u)

    def add_prob(self, node, cond_nodes, prob):
        # D=T, ['B=T', 'C=T'], 0.1
        node, node_val = node[0], node[2]

        if node_val=='F':
            prob = 1 - float(prob)
        else:
            prob = float(prob)

        if not cond_nodes:
            self.bn[node]['cond_prob'][None] = prob
        else:
            bag = { x[0]:x[2] for x in cond_nodes } # { B:T, C:T }
            pairs = [ bag[pa] for pa in self.bn[node]['parents']] # [T,T] in parents order
            pairs = [True if x=='T' else False for x in pairs] # [1,1]
            self.bn[node]['cond_prob'][tuple(pairs)] = prob

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
            s = s.rstrip('\n').lstrip('P(').replace(')=','|').replace(',','|').split('|')
            node, cond_nodes, prob = s[0], s[1:-1] ,s[-1]
            BN.add_prob(node, cond_nodes, prob)
    return BN

def read_input(fname):
    pass


# Program
def enumerate_ask():
    pass

def enumerate_all():
    pass


# Utils
def normalize():
    pass

def print_res(res):
    pass


def main():
    # bn = BN("test/bn.txt")
    BN = read_bn("tests/bn.txt")
    print BN
    Q,E = read_input("tests/input.txt")
    res = enumerate_ask(Q,E,BN)
    print_res(res)


if __name__ == '__main__':
    main()


