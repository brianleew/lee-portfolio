import re


class Calculator(object):

    def add(self, string: str) -> int:
        # handle empty string
        if string == "":
            return 0

        if string.isdigit():
            return int(string)

        # handle comma separated values, for example "1,2"
        # split the input string into an array using split
        numbers = re.split(",|\n", string)
        # numbers = string.split(",")
        # convert each string in the array into an int
        numbers = [int(n) for n in numbers]
        # sum all the ints in the array
        return sum(numbers)


