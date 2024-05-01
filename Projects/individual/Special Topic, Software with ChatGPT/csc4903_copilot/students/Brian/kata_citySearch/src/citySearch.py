# Implement a city search functionality.
# The function takes a string (search text) as input and returns the found cities which corresponds to the search text.
class CitySearch(object):
    def search(self, string: str):
        # Create a collection of strings that will act as a DB for the city names
        city_names = ["Paris", "Budapest", "Skopje", "Rotterdam", "Valencia", "Vancouver", "Amsterdam", "Vienna",
                      "Sydney", "New York City", "London", "Bangkok", "Hong Kong", "Dubai", "Rome", "Istanbul"]
        # 5. If the search text is a “*” (asterisk), then it should return all the city names.
        if string == "*":
            return city_names
        # 1. If the search text is fewer than 2 characters, then should return no results.
        #       (It is an optimization feature of the search functionality.)
        if len(string) < 2:
            raise Exception("no result")
        # 2. If the search text is equal to or more than 2 characters, then it should return all the city names starting with the exact search text.
        # For example for search text “Va”, the function should return Valencia and Vancouver
        if len(string) >= 2:
            lowercase_search_text = string.lower()
            # 3. case in-sensitive
            # matching_cities = [city for city in city_names if city.lower().startswith(lowercase_search_text)]
            matching_cities = [city for city in city_names if lowercase_search_text in city.lower()] # 4. search text part of name
            result = " and ".join(matching_cities)
            return result

