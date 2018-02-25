#!/usr/bin/env python

import csv
from itertools import combinations
import time

"""Sudoku game using arc-consistency check"""

Debug = False


class CSP:
    """Define csp
    varialbes: [var1, var2, ...]
    domain: { var1:set() var2:set() }
    constraint (neighbors): {var1:}
    """
    def __init__(self, variables, domains, constraints):
        self.variables = variables
        self.domains = domains
        self.constraints = constraints

    def __str__(self):
        return str(self.variables) + str(self.domains)

    def show(self):
        """Print out variables with domain size 1"""
        cnt = 0
        s = ""
        for x in self.variables:
            if len(self.domains[x]) == 1:
                s += "%s " % x
                cnt += 1
        print("%s \t size-1 domain: %s / %s" % (s, cnt, len(self.variables)))

    def get_init_assignment(self):
        """Return dict of assignment which are specified initially"""
        assignment = {}
        for x in self.variables:
            if len(self.domains[x]) == 1:
                assignment[x] = list(self.domains[x])[0]
        return assignment

# CSP Processing
def goal_test(assignment, csp):
    """Check if all variables are assigned"""
    for var in csp.variables:
        if len(csp.domains[var]) != 1 or var not in assignment:
            return False
    return True

def get_domain(var, csp):
    return csp.domains[var].copy()

def check_constraints(assignment, new_var, new_value, csp):
    """Check if new_value violates its neighbor"""
    if Debug:
        if new_var == 'B9':
            print("%s %s %s %s" % (new_var, new_value, len(assignment), csp.domains['B9']))
        else:
            print("%s %s %s" % (new_var, new_value, len(assignment)))

    for var, value in assignment.iteritems():
        if new_var in csp.constraints[var] and new_value == value:
            return False
    return True

def check_consistency(csp):
    """Check if any variable is empty (because fo ac3)"""
    for key, val in csp.domains.iteritems():  # empty domains happens when filtering
        if not val:
            return False
    return True

def assign_variable(assignment, var, value, csp):
    """Add assignment, remove domain, return a removal dict for recovery"""
    assignment[var] = value
    removal = dict()
    removal[var] = {val for val in csp.domains[var]
                    if val != value}  # set of store other values
    csp.domains[var] = {value}  # assign value
    return removal


# CSP Search (Backtracking)
def backtrack_search_solver(csp, apply_ac3=False, apply_mrv=False):
    """Backtracking search
    apply_ac3: True if apply ac3
    apply_mrv: True if apply mrv, speed up a lot

    Return assignment if csp solved, False if failed
    """
    # assignment = {}
    assignment = csp.get_init_assignment()
    return backtrack_search(assignment, csp, apply_ac3, apply_mrv)

def backtrack_search(assignment, csp, apply_ac3, apply_mrv):
    """
    Recursive of backtracking search
    domain reduction happens when: 1.assignment 2.ac3 (filtering)

    assign -> ac3 filtering -> assign -> ...

    Maintain a removal list for [assignment/var's domain] recovery
    """
    if goal_test(assignment, csp):
        return assignment

    var = select_minimum_remaining_variable(assignment, csp) if apply_mrv \
        else select_first_variable(assignment, csp)

    for value in get_domain(var, csp):

        if check_constraints(assignment, var, value, csp):  # check consistency

            assign_removal = assign_variable(assignment, var, value, csp)

            if apply_ac3:
                # add x -> var (x: neighbors)
                queue = [(x, var) for x in csp.constraints[var]]
                ac3_removal = ac3_filtering(csp, queue)

            if check_consistency(csp):  # ac3 might result in empty domains
                result = backtrack_search(assignment, csp, apply_ac3, apply_mrv)
                if result:
                    return result

            removal = merge_removals(
                assign_removal, ac3_removal, var) if apply_ac3 else assign_removal

            # when branch fail: recover assignment & vars' domains
            for k, v in removal.iteritems():
                csp.domains[k] = csp.domains[k] | v
            del assignment[var]
    return False

# CSP Ordering
def select_first_variable(assignment, csp):
    """Return the first variable in unassigned list"""
    unassigned_set = set(csp.variables) - set(assignment.keys())
    return list(unassigned_set)[0]

def select_minimum_remaining_variable(assignment, csp):
    """Return the unassigned variable with the smallest domain"""
    unassigned_set = set(csp.variables) - set(assignment.keys())
    mrv_list = []
    for var in unassigned_set:
        mrv_list.append( (len(csp.domains[var]),var) )
    return min(mrv_list)[1]

# CSP Filtering
def ac3_filtering(csp, queue=None):
    """Return a reduced-domain csp given queue (x,y)
    key idea: For x -> y, check x,y's domains, and remove x's val if necessary

    Required consistency check after this method
    Return a removal dict for recovery
    """
    if not queue:  # for preprocessor
        queue = []
        for var1, neighbors in csp.constraints.iteritems():
            for var2 in neighbors:
                queue.append((var1, var2))
    removal = dict()
    while queue:
        x, y = queue.pop()
        # some revision done on x's domain
        if remove_inconsistent_values(x, y, removal, csp):
            queue = queue + [(z, x) for z in csp.constraints[x]]
    return removal


def remove_inconsistent_values(x, y, removal, csp):
    """Check x, y domain, remove from x's if necessary
    Return True if there is any revision on x
    """
    revision = False  # check if any revision occurs
    x_domain = csp.domains[x].copy()  # might change
    y_domain = csp.domains[y]
    for x_val in x_domain:
        if not y_domain - {x_val}:
            csp.domains[x].remove(x_val)
            revision = True
            if x not in removal:
                removal[x] = {x_val}
            else:
                removal[x] = removal[x] | {x_val}
    return revision


def merge_removals(assign_removal, ac3_removal, var):
    """Merge removals from assignment and ac3"""
    merge_dict = ac3_removal.copy()

    if var in merge_dict and var in ac3_removal:
        merge_dict[var] = assign_removal[var] | ac3_removal[var]
    elif var in assign_removal:
        merge_dict[var] = assign_removal[var]
    return merge_dict

# -------------------------------
# Sudoku methods
def load_sudoku(input_file):
    """from file
    define board row: A-I, col: 1-9

    varialbes: [A1, A2, ...]
    domains: { A1:{1,2,3..9} A2:{1,2,3...9} }
    constraints (neighbors): {A1:{A2,B1,...}, A2:{A1,..} }

    """
    rows = 'ABCDEFGHI'
    cols = '123456789'

    variables = [x + y for x in rows for y in cols]

    # Construct domain, careful: we used string instead of int
    domains = {x + y: {'1', '2', '3', '4', '5', '6', '7', '8', '9'}
               for x in rows for y in cols}  # default

    with open(input_file, 'r') as f:
        csv_reader = csv.reader(f)
        sudoku_mat = list(csv_reader)  # list-of-list

    for i, row in enumerate(sudoku_mat):
        for j, val in enumerate(row):
            if val != '0':
                sym = rows[i] + cols[j]  # A1
                domains[sym] = {val}

    # Construct constraints using all neighbor pairs
    neighbor_pairs = []  # add all pairs (a,b) in row, col, box, but not (b,a)
    # row
    for x in rows:
        sym_row = [x + y for y in cols]  # eg: A1-A9
        neighbor_pairs.extend(combinations(sym_row, 2))

    # col
    for y in cols:
        sym_col = [x + y for x in rows]  # eg: A1-I1
        neighbor_pairs.extend(combinations(sym_col, 2))

    # 3x3 box
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            sym_box = [x + y for x in rows[i:i + 3] for y in cols[j:j + 3]]
            neighbor_pairs.extend(combinations(sym_box, 2))

    constraints = {x: set() for x in variables}  # initialize
    for x, y in neighbor_pairs:
        constraints[x].add(y)
        constraints[y].add(x)

    return CSP(variables, domains, constraints)

def write_sudoku(output_file, assignment):
    """Write a csv file given dict of assigments"""
    with open(output_file, 'w') as f:
        csv_writer = csv.writer(f)

        row = ''
        # 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7'...
        for i, sym in enumerate(sorted(assignment)):
            row += "%s" % assignment[sym]
            if (i + 1) % 9 == 0:
                csv_writer.writerow(row)
                row = ''
            else:
                row += ''


def main():
    """Define csp, run backtracking and use AC-3 filtering"""

    sudoku_file = "tests/suinput_very_hard.csv"
    output_file = "suoutput.csv"

    csp = load_sudoku(sudoku_file)
    if Debug:
        csp.show()

    t_0 = time.time()
    queue = [(x, var) for var in csp.get_init_assignment()
             for x in csp.constraints[var]]
    ac3_filtering(csp, queue)  # preprocessor
    result = backtrack_search_solver(csp, apply_ac3=True, apply_mrv=True)
    if Debug:
        csp.show()
    print("Runtime: %s" % (time.time() - t_0))

    if result:
        write_sudoku(output_file, result)
        print("Sudoku solved")
    else:
        print("Invalid board")


if __name__ == '__main__':
    main()
