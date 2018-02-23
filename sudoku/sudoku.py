#!/usr/bin/env python

import csv
from itertools import combinations
import time

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
    # if len(assignment) != len(csp.variables):
    #      return False

    for var in csp.variables:
        if len(csp.domains[var]) != 1 or var not in assignment:
            return False
    return True
    # for key, val in csp.domains.iteritems():
    #     if len(val) == 0:
    #         return False
    # return True

def get_domain(var, csp):
    return csp.domains[var].copy()

def check_constraints(assignment, new_var, new_value, csp):
    print new_var, new_value, len(assignment) # debug
    for var, value in assignment.iteritems():
        if new_var in csp.constraints[var] and new_value==value:
            return False
    return True

def check_consistency(csp):
    for key, val in csp.domains.iteritems(): # empty domains happens when filtering
        if len(val) == 0:
            return False
    return True

def assign_variable(assignment, var, value, csp):
    """return a removal dict"""
    assignment[var] = value
    # removal_vals =
    removal = dict()
    removal[var] = { val for val in csp.domains[var] if val != value } # set of store other values
    csp.domains[var] = {value}  # assign value
    return removal

# csp search
def backtrack_search_solver(csp, filter_or_not=False):
    """Backtracking search
    filter_or_not -> ac3
    return solution
    """
    # assignment = {}
    assignment = csp.get_init_assignmnet()
    result = backtrack_search(assignment, csp, filter_or_not)
    print assignment, len(assignment)
    return result

def backtrack_search(assignment, csp, filter_or_not):
    """
    domain reduction happens: 1.assignment 2.ac3 (filtering)
    required a removal list for recovery
    """
    if goal_test(assignment, csp):
        return assignment
    var = select_variable(assignment, csp)
    # print var
    for value in get_domain(var, csp):
        if var == 'D7' and value == '2':
            print check_constraints(assignment, var, value, csp)

        if check_constraints(assignment, var, value, csp): # check consistency

            # assign
            assign_removal = assign_variable(assignment, var, value, csp)



            # filter: might result in empty domains
            if filter_or_not:
                queue = [(x,var) for x in csp.constraints[var]] # check x -> var
                ac3_removal = AC3_filter(csp, queue)
                # csp.show()

            # if var == 'D7' and value == '2':
            #     print assign_removal, ac3_removal, check_consistency(csp), csp.domains['D7']
            #     for x,v in csp.domains.iteritems():
            #         if len(v) == 0:
            #             print x, v

            if check_consistency(csp): # need to check after ac3
                result = backtrack_search(assignment, csp, filter_or_not)
                if result:
                    return result

            removal = merge_two_dicts(assign_removal, ac3_removal) if filter_or_not else assign_removal

            # branch fail: recover assignment & vars' domains
            for k,v in removal.iteritems():
                csp.domains[k] = csp.domains[k] | v
            del assignment[var]
    return False

# csp ordering
def select_variable(assignment, csp):
    unassigned_set = set(csp.variables) - set(assignment.keys())
    return list(unassigned_set)[0]

# csp filtering
def AC3_filter(csp, queue=None):
    """return a reduced-domain csp
    queue (x,y) : check each x -> y
    required consistency check after this method

    return a removal dict for recovery
    """
    if not queue: # for preprocessor
        queue = []
        for var1, neighbors in csp.constraints.iteritems():
            for var2 in neighbors:
                queue.append((var1,var2))
    removal = dict()
    # print queue[-1]
    while queue:
        x,y = queue.pop()
        if remove_inconsistent_values(x,y, removal, csp): # done some revision on x's domain
            queue = queue + [ (z,x) for z in csp.constraints[x] ]
    return removal

def remove_inconsistent_values(x, y, removal, csp):
    """Check x, y domain, remove from x's if necessary"""
    revision = False # check if any revision done
    x_domain = csp.domains[x].copy() # might change
    # print csp.domains, y
    y_domain = csp.domains[y]
    for x_val in x_domain:
        if not (y_domain - {x_val}):
            csp.domains[x].remove(x_val)
            revision = True
            if x not in removal:
                removal[x] = { x_val }
            else:
                removal[x] = removal[x] | { x_val }
    return revision

def merge_two_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z

def main():
    """Define csp, run backtracking and use AC-3 filtering"""

    sudoku_file = "tests/suinput_easy.csv"
    output_file = "suoutput.csv"

    csp = load_sudoku(sudoku_file)
    csp.show()

    t0 = time.time()
    init_assignments = csp.get_init_assignmnet()
    queue = [(x,var) for var in init_assignments for x in csp.constraints[var]]
    AC3_filter(csp,queue) # preprocessor
    result = backtrack_search_solver(csp, filter_or_not=True)
    print "runtime: %s" % (time.time() - t0)
    if result:
        write_sudoku(output_file, result)
        csp.show()
        print "Sudoku solved"
    else:
        csp.show()
        print "error"

    # print csp.domains


if __name__ == '__main__':
    main()