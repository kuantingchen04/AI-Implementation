import unittest
import cell

class TestCA(unittest.TestCase):
    # num_cell = 10 # should be >= 2
    # num_gen = 100 # should be >= 0
    # CA(num_cell, num_gen)
    def test_input(self):
        cell.CA(-2,10)

    def test_rule(self):
        cell.rule
        pass


if __name__ == '__main__':
    unittest.main()