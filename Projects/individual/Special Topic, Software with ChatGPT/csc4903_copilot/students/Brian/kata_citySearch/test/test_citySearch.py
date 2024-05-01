from unittest import TestCase
from citySearch import CitySearch

class TestCitySearch(TestCase):

    def setUp(self) -> None:
        self.srch = CitySearch()

    def test_srchTextLt2NoRes(self): #1
        with self.assertRaises(Exception):
            self.srch.search("F") # less than 2 so 1 character
            self.srch.search("") # less than 2 so 0 character

    def test_searchText2PlusChars(self): #2
        self.assertEqual("Valencia and Vancouver", self.srch.search("Va")) # capital/lower case not checked atm

    def test_caseInsensitive(self): #3
        self.assertEqual("Valencia and Vancouver", self.srch.search("va"))

    def test_searchTextPartOfName(self): #4
        self.assertEqual("Budapest", self.srch.search("ape"))

    def test_ifSearchTextIsAsterisk(self): #5
        city_names = ["Paris", "Budapest", "Skopje", "Rotterdam", "Valencia", "Vancouver", "Amsterdam", "Vienna",
                      "Sydney", "New York City", "London", "Bangkok", "Hong Kong", "Dubai", "Rome", "Istanbul"]
        self.assertEqual(city_names, self.srch.search("*"))
