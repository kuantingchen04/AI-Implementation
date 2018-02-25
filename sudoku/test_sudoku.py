import unittest

from sudoku import load_sudoku, backtrack_search_solver
import numpy as np

# too hard? might sol might vary?
def check_sol(val_list):
    # val_list = ['7', '9', '8', '4', '1', '3', '5', '6', '2', '6', '3', '4', '2', '5', '8', '9', '1', '7',
    #        '5', '1', '2', '7', '6', '9', '3', '8', '4', '1', '7', '9', '8', '4', '5', '2', '3', '6',
    #        '4', '8', '6', '3', '2', '1', '7', '9', '5', '2', '5', '3', '9', '7', '6', '1', '4', '8',
    #        '3', '6', '1', '5', '8', '7', '4', '2', '9', '8', '4', '5', '1', '9', '2', '6', '7', '3',
    #        '9', '2', '7', '6', '3', '4', '8', '5', '1']

    val_list = [ int(x) for x in val_list ]
    valid_set = {1, 2, 3, 4, 5, 6, 7, 8, 9}

    val_mat = []
    for i in range(0,81,9):
        val_mat.append(val_list[i:i+9])

    val_mat = np.array(val_mat)

    # Check col
    for j in range(9):
        if set( val_mat[:,j].flatten() ) != valid_set:
            return False

    for i in range(9):
        if set(val_mat[i, :].flatten()) != valid_set:
            return False

    for i in range(0,9,3):
        for j in range(0,9,3):
            if set(val_mat[i:i+3,j:j+3].flatten()) != valid_set:
                return False
    return True

class TestSudoku(unittest.TestCase):


    def test_backtrack_easy(self):
        csp = load_sudoku("tests/suinput_easy.csv")

        result = backtrack_search_solver(csp, False)
        self.assertTrue(result)

        val_list = [ val for (key, val) in sorted(result.iteritems()) ]
        self.assertTrue(check_sol(val_list))


    def test_arc_only_very_easy(self):
        csp = load_sudoku("tests/suinput_very_easy.csv")

        result = backtrack_search_solver(csp, True)
        self.assertTrue(result)

        val_list = [ val for (key, val) in sorted(result.iteritems()) ]
        self.assertTrue(check_sol(val_list))

    def test_arc_backtrack_easy(self):
        csp = load_sudoku("tests/suinput_easy.csv")
        result = backtrack_search_solver(csp, True)

        self.assertTrue(result)

        val_list = [ val for (key, val) in sorted(result.iteritems()) ]
        self.assertTrue(check_sol(val_list))

    def test_mrv_only_easy(self):
        csp = load_sudoku("tests/suinput_easy.csv")

        result = backtrack_search_solver(csp, False, True)
        self.assertTrue(result)

        val_list = [ val for (key, val) in sorted(result.iteritems()) ]
        self.assertTrue(check_sol(val_list))

if __name__ == '__main__':
    unittest.main()