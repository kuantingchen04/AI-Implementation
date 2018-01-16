import unittest
import cell

class TestCA(unittest.TestCase):

    def test_input(self):
        cell.CA(-2,10)

    def test_rule(self):
        cell.rule
        pass


if __name__ == '__main__':
    unittest.main()