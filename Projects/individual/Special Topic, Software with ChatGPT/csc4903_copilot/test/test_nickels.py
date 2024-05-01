from unittest import TestCase
from src.nickels import nickels_and_pennies


class Test(TestCase):
    def test_nickels_and_pennies(self):
        self.assertEqual([1, 3], nickels_and_pennies(2, 3, 8))

    def test_nickels_1(self):
        self.assertEqual([1, 7], nickels_and_pennies(1, 13, 12))

    def test_nickels_2(self):
        self.assertEqual([-1, -1], nickels_and_pennies(3, 2, 14))

