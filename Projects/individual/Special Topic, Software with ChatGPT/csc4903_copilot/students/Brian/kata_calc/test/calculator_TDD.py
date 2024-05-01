from unittest import TestCase
from calculator import Calculator


class TestCalculator(TestCase):

    def setUp(self) -> None:
        self.calc = Calculator()

    def test_add_empty(self): #1
        self.assertEqual(0, self.calc.add(""))
    def test_add_single(self):
        self.assertEqual(1, self.calc.add("1"))
    def test_add_pair(self):
        self.assertEqual(3, self.calc.add("2,1"))
    def test_add_pairplus(self): #2
        self.assertEqual(6, self.calc.add("1,2,3"))
    def test_add_NLorCOMMAasDelim(self): #3
        self.assertEqual(6, self.calc.add("1,2\n3"))
        with self.assertRaises(Exception):
            self.calc.add("2,\n3")
    def test_throwException(self): #4
        with self.assertRaises(Exception):
            self.calc.add("1,2,")
    def test_handleDiffDelim(self): #5
        self.assertEqual(4, self.calc.add("//;\n1;3"))
        self.assertEqual(6, self.calc.add("//|\n1|2|3"))
        self.assertEqual(7, self.calc.add("//sep\n2sep5"))
    def test_handleDiffDelimException(self): #5
        with self.assertRaises(Exception):
            self.calc.add("//|\n1|2,3")
    def test_DetectNegNum(self): #6
        with self.assertRaises(Exception):
            self.calc.add("1,-2")
        with self.assertRaises(Exception):
            self.calc.add("2,-4,-9")
    def test_returnALLerrorMsg(self): #7
        with self.assertRaises(Exception):
            self.calc.add("//|\n1|2,-3")
    def test_biggerThan1000(self): #8
        self.assertEqual(2, self.calc.add("2,1001"))