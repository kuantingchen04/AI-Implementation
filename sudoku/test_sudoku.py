import unittest

from sudoku import load_sudoku, backtrack_search_solver

# too hard? might sol might vary?

class TestSudoku(unittest.TestCase):

    # self.filter_or_not = True

    def test_result_592(self):
        sudoku_file = "tests/suinput_592.csv"

        csp = load_sudoku(sudoku_file)
        result = backtrack_search_solver(csp, False)

        self.assertTrue(result)

        val_list = [ val for (key, val) in sorted(result.iteritems()) ]
        sol = ['4', '8', '6', '5', '1', '9', '3', '7', '2', '1', '9', '7', '3', '6', '2', '5', '4', '8', '3', '2', '5', '7', '4', '8', '9', '6', '1', '8', '4', '9', '6', '2', '3', '1', '5', '7', '7', '6', '3', '9', '5', '1', '2', '8', '4', '5', '1', '2', '4', '8', '7', '6', '3', '9', '6', '7', '4', '1', '9', '5', '8', '2', '3', '9', '5', '8', '2', '3', '4', '7', '1', '6', '2', '3', '1', '8', '7', '6', '4', '9', '5']

        self.assertEqual(val_list,sol)

    def test_result_very_easy(self):
        sudoku_file = "tests/suinput_very_easy.csv"

        csp = load_sudoku(sudoku_file)
        result = backtrack_search_solver(csp, False)

        self.assertTrue(result)

        val_list = [ val for (key, val) in sorted(result.iteritems()) ]
        sol = ['3', '8', '6', '7', '9', '2', '5', '1', '4', '9', '4', '1', '5', '3', '8', '7', '6', '2', '5', '2', '7', '1', '4', '6', '3', '8', '9', '1', '7', '4', '9', '6', '3', '2', '5', '8', '8', '5', '2', '4', '1', '7', '9', '3', '6', '6', '3', '9', '2', '8', '5', '4', '7', '1', '4', '9', '3', '8', '5', '1', '6', '2', '7', '7', '1', '5', '6', '2', '9', '8', '4', '3', '2', '6', '8', '3', '7', '4', '1', '9', '5']

        self.assertEqual(val_list,sol)

    def test_result_easy(self):
        sudoku_file = "tests/suinput_easy.csv"

        csp = load_sudoku(sudoku_file)
        result = backtrack_search_solver(csp, False)

        self.assertTrue(result)

        val_list = [ val for (key, val) in sorted(result.iteritems()) ]
        sol = ['7', '9', '8', '4', '1', '3', '5', '6', '2', '6', '3', '4', '2', '5', '8', '9', '1', '7', '5', '1', '2', '7', '6', '9', '3', '8', '4', '1', '7', '9', '8', '4', '5', '2', '3', '6', '4', '8', '6', '3', '2', '1', '7', '9', '5', '2', '5', '3', '9', '7', '6', '1', '4', '8', '3', '6', '1', '5', '8', '7', '4', '2', '9', '8', '4', '5', '1', '9', '2', '6', '7', '3', '9', '2', '7', '6', '3', '4', '8', '5', '1']

        self.assertEqual(val_list,sol)

    def test_result_592_ac3(self):
        sudoku_file = "tests/suinput_592.csv"

        csp = load_sudoku(sudoku_file)
        result = backtrack_search_solver(csp, True)

        self.assertTrue(result)

        val_list = [ val for (key, val) in sorted(result.iteritems()) ]
        sol = ['4', '8', '6', '5', '1', '9', '3', '7', '2', '1', '9', '7', '3', '6', '2', '5', '4', '8', '3', '2', '5', '7', '4', '8', '9', '6', '1', '8', '4', '9', '6', '2', '3', '1', '5', '7', '7', '6', '3', '9', '5', '1', '2', '8', '4', '5', '1', '2', '4', '8', '7', '6', '3', '9', '6', '7', '4', '1', '9', '5', '8', '2', '3', '9', '5', '8', '2', '3', '4', '7', '1', '6', '2', '3', '1', '8', '7', '6', '4', '9', '5']

        self.assertEqual(val_list,sol)

    def test_result_very_easy_ac3(self):
        sudoku_file = "tests/suinput_very_easy.csv"

        csp = load_sudoku(sudoku_file)
        result = backtrack_search_solver(csp, True)

        self.assertTrue(result)

        val_list = [ val for (key, val) in sorted(result.iteritems()) ]
        sol = ['3', '8', '6', '7', '9', '2', '5', '1', '4', '9', '4', '1', '5', '3', '8', '7', '6', '2', '5', '2', '7', '1', '4', '6', '3', '8', '9', '1', '7', '4', '9', '6', '3', '2', '5', '8', '8', '5', '2', '4', '1', '7', '9', '3', '6', '6', '3', '9', '2', '8', '5', '4', '7', '1', '4', '9', '3', '8', '5', '1', '6', '2', '7', '7', '1', '5', '6', '2', '9', '8', '4', '3', '2', '6', '8', '3', '7', '4', '1', '9', '5']

        self.assertEqual(val_list,sol)

    def test_result_easy_ac3(self):
        sudoku_file = "tests/suinput_easy.csv"

        csp = load_sudoku(sudoku_file)
        result = backtrack_search_solver(csp, True)

        self.assertTrue(result)

        val_list = [ val for (key, val) in sorted(result.iteritems()) ]
        sol = ['7', '9', '8', '4', '1', '3', '5', '6', '2', '6', '3', '4', '2', '5', '8', '9', '1', '7', '5', '1', '2', '7', '6', '9', '3', '8', '4', '1', '7', '9', '8', '4', '5', '2', '3', '6', '4', '8', '6', '3', '2', '1', '7', '9', '5', '2', '5', '3', '9', '7', '6', '1', '4', '8', '3', '6', '1', '5', '8', '7', '4', '2', '9', '8', '4', '5', '1', '9', '2', '6', '7', '3', '9', '2', '7', '6', '3', '4', '8', '5', '1']

        self.assertEqual(val_list,sol)

if __name__ == '__main__':
    unittest.main()