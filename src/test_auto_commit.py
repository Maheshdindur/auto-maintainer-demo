import unittest
from app import add

class TestApp(unittest.TestCase):

    def test_add_positive_numbers(self):
        self.assertEqual(add(1, 2), 3)
        self.assertEqual(add(10, 20), 30)

    def test_add_negative_numbers(self):
        self.assertEqual(add(-1, -2), -3)
        self.assertEqual(add(-10, -5), -15)

    def test_add_positive_and_negative(self):
        self.assertEqual(add(5, -3), 2)
        self.assertEqual(add(-7, 4), -3)

    def test_add_with_zero(self):
        self.assertEqual(add(0, 5), 5)
        self.assertEqual(add(5, 0), 5)
        self.assertEqual(add(0, 0), 0)
        self.assertEqual(add(-5, 0), -5)

    def test_add_floating_point_numbers(self):
        self.assertAlmostEqual(add(1.1, 2.2), 3.3)
        self.assertAlmostEqual(add(-1.5, 3.0), 1.5)

if __name__ == '__main__':
    unittest.main()