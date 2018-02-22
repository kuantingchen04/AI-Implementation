#!/usr/bin/env python

import csv
from itertools import combinations

"""Sudoku game"""

class CSP:

    def __init__(self, variables, domains, constraints):
        """varialbes: [var1, var2, ...]
        domain: { var1:set() var2:set() }
        constraint (neighbors): {var1:}
        """

        self.variables = variables
        self.domains = domains
        self.constraints = constraints

    def __str__(self):
        return str(self.variables) + str(self.domains)


# -------------------------------
# sudoku methods

def load_sudoku(input_file):
    """from file
    define board row: A-I, col: 1-9

    varialbes: [A1, A2, ...]
    domains: { A1:{1,2,3..9} A2:{1,2,3...9} }
    constraints (neighbors): {A1:{A2,B1,...}, A2:{A1,..} }

    """
    rows = 'ABCDEFGHI'
    cols = '123456789'

    variables = [ x+y for x in rows for y in cols ]

    # Construct domain
    domains = { x+y: {1,2,3,4,5,6,7,8,9} for x in rows for y in cols } # default

    with open(input_file, 'r') as f:
        csv_reader = csv.reader(f)
        sudoku_mat = list(csv_reader) # list-of-list

    for i, row in enumerate(sudoku_mat):
        for j, val in enumerate(row):
            if val != '0':
                sym = rows[i] + cols[j] # A1
                domains[sym] = { val }

    # Construct constraints using all neighbor pairs
    neighbor_pairs = [] # add all pairs (a,b) in row, col, box, but not (b,a)
    # row
    for x in rows:
        sym_row = [ x+y for y in cols ] # eg: A1-A9
        neighbor_pairs.extend(combinations(sym_row, 2))

    # col
    for y in cols:
        sym_col = [ x+y for x in rows ] # eg: A1-I1
        neighbor_pairs.extend(combinations(sym_col, 2))

    # 3x3 box
    for i in range(0,9,3):
        for j in range(0,9,3):
            sym_box = [ x+y for x in rows[i:i+3] for y in cols[j:j+3] ]
            neighbor_pairs.extend(combinations(sym_box, 2))

    constraints = { x:set() for x in variables } # initialize
    for x,y in neighbor_pairs:
        constraints[x].add(y)
        constraints[y].add(x)

    return CSP(variables, domains, constraints)

def show_sudoku(csp):
    cnt = 0
    for x in csp.variables:
        domain_set = csp.domains[x]
        if len(domain_set) == 1:
            print "%s: %s" % (x,list(domain_set)[0]),
            cnt += 1
        elif len(domain_set) == 0:
            print "%s: %s" % (x, 'X')
    print "\t fill: %s / 81" %  cnt
    print csp.domains['A1']
    print csp.constraints['A1']

# -------------------------------
# csp processor

def AC3_filter(csp):
    """return a reduced-domain csp"""
    return csp

def backtrack_solver(csp):
    """return solution"""

    AC3_filter(csp)
    return csp



def main():
    """Define csp, run backtracking and use AC-3 filtering"""

    sudoku_file = "suinput.csv"
    csp = load_sudoku(sudoku_file)
    show_sudoku(csp)

    backtrack_solver(csp)


if __name__ == '__main__':
    main()