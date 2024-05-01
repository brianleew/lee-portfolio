from unittest import TestCase
from src.main import Calculator


class TestCalculator(TestCase):

    def setUp(self) -> None:
        self.calc = Calculator()

    def test_add_empty(self):
        self.assertEqual(0, self.calc.add(""))

    def test_add_one(self):
        self.assertEqual(1, self.calc.add("1"))

    def test_add_pair(self):
        self.assertEqual(3, self.calc.add("1,2"))

    def test_add_sequence(self):
        self.assertEqual(5, self.calc.add("1,2,2"))

    def test_add_newline(self):
        self.assertEqual(5, self.calc.add("1,2\n2"))

    def test_add_bad_string(self):
        with self.assertRaises(Exception):
            self.calc.add("1,\n2")
            self.calc.add("1,2,")

    def test_add_delimiter(self):
        self.assertEqual(4, self.calc.add("//;\n1;3"))
        self.assertEqual(6, self.calc.add("//|\n2|3"))
        self.assertEqual(7, self.calc.add("//sep\n2sep5"))
