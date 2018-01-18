import unittest
import cell

class TestCA(unittest.TestCase):
    # CA(num_cell, num_gen)
    def test_invalid_input(self):
        # Left violate
        self.assertRaises(ValueError, cell.CA, 2.5, 2)
        self.assertRaises(ValueError, cell.CA, 1, 2)  # problem?
        self.assertRaises(ValueError, cell.CA, -1, 2)

        # Right violate
        self.assertRaises(ValueError, cell.CA, 2, 2.5)
        self.assertRaises(ValueError, cell.CA, 2, -1)

    def test_rule(self):
        self.assertEqual(cell.rules(0, 0, 0), 0)
        self.assertEqual(cell.rules(0, 0, 1), 1)
        self.assertEqual(cell.rules(0, 1, 0), 0)
        self.assertEqual(cell.rules(0, 1, 1), 0)
        self.assertEqual(cell.rules(1, 0, 0), 1)
        self.assertEqual(cell.rules(1, 0, 1), 0)
        self.assertEqual(cell.rules(1, 1, 0), 0)
        self.assertEqual(cell.rules(1, 1, 1), 0)

if __name__ == '__main__':
    unittest.main()