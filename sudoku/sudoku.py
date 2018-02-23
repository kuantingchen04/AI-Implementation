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
        # self.log = []

    def __str__(self):
        return str(self.variables) + str(self.domains)

    # def goal_test(self, assignment):
    #     return len(assignment) == len(self.variables)

    # def get_domain(self, var):
    #     return self.domains[var].copy()

    # def check_constraints(self, assignment, new_var, new_value):
    #     # print new_var, new_value # debug
    #     for var, value in assignment.iteritems():
    #         if new_var in self.constraints[var] and new_value==value:
    #             return False
    #     return True

    # csp ordering
    # def select_variable(self, assignment):
    #     unassigned_set = set(self.variables) - set(assignment.keys())
    #     return list(unassigned_set)[0]

    def show(self):
        cnt = 0
        for x in self.variables:
            if len(self.domains[x]) == 1:
                print x,
                cnt += 1
        print "\t size-1 domain: %s / %s" % (cnt, len(self.variables))
        # print self.domains['A1']

    def get_init_assignmnet(self):
        assignment = {}
        for x in self.variables:
            if len(self.domains[x]) == 1:
                assignment[x] = list(self.domains[x])[0]
        return assignment


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

    # Construct domain, careful: we used string instead of int
    domains = { x+y: {'1','2','3','4','5','6','7','8','9'} for x in rows for y in cols } # default

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

def write_sudoku(output_file, assignment):

    with open(output_file, 'w') as f:
        csv_writer = csv.writer(f)

        row = ''
        for i, sym in enumerate(sorted(assignment)): # 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7'...
            row += "%s" % assignment[sym]
            if (i + 1) % 9 == 0:
                csv_writer.writerow(row)
                row = ''
            else:
                row += ''

# -------------------------------
## csp processing

# csp basics
def goal_test(assignment, csp):
    return len(assignment) == len(csp.variables)

def get_domain(var, csp):
    return csp.domains[var].copy()

def check_constraints(assignment, new_var, new_value, csp):
    # print new_var, new_value # debug
    for var, value in assignment.iteritems():
        if new_var in csp.constraints[var] and new_value==value:
            return False
    return True


# csp search
def backtrack_solver(csp):
    """Backtracking search
    return solution"""
    # assignment = {}
    assignment = csp.get_init_assignmnet()
    return backtrack(assignment, csp)

def backtrack(assignment, csp):
    if goal_test(assignment, csp):
        return assignment
    var = select_variable(assignment, csp)
    # print var
    for value in get_domain(var, csp):
        if check_constraints(assignment, var, value, csp): # T: consistent
            assignment[var] = value
            result = backtrack(assignment, csp)
            if result:
                return result
            del assignment[var]
    return False
    # AC3_filter(csp)
    # return csp


# csp ordering
def select_variable(assignment, csp):
    unassigned_set = set(csp.variables) - set(assignment.keys())
    return list(unassigned_set)[0]

# csp filtering
def AC3_filter(csp):
    """return a reduced-domain csp"""
    return csp



def main():
    """Define csp, run backtracking and use AC-3 filtering"""

    sudoku_file = "suinput.csv"
    output_file = "suoutput.csv"

    csp = load_sudoku(sudoku_file)
    csp.show()
    result = backtrack_solver(csp)
    if result:
        write_sudoku(output_file, result)
        csp.show()
        print "Sudoku solved"
    else:
        print "error"

if __name__ == '__main__':
    main()