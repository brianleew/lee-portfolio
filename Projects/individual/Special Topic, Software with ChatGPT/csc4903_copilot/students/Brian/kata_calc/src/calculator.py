import re


class Calculator(object):

    def add(self, string: str) -> int:
        error_messages = []

        if string == "":
            return 0
        if string.isdigit():
            return int(string)

        negative_matches = re.findall(r'-\d+', string)
        if negative_matches:
            error_messages.extend(
                ["Negative numbers not allowed: " + negative_value for negative_value in negative_matches])

        delimiter = "[,\n]"
        if re.search(delimiter, string) and (string.endswith(",") or string.endswith("\n")):
            error_messages.append("Extra delimiter at the end.")
        if re.search(delimiter, string) and (string.startswith(",") or string.startswith("\n")):
            error_messages.append("Extra delimiter at the beginning.")

        if re.search(r'([,\\n]{2,})', string):
            error_messages.append("Consecutive delimiters in between digits.")

        if re.search(r'//(.*)\n', string):
            match = re.search(r'//(.*)\n', string)
            delim = match.group(1)
            new_string = string.removeprefix(match.group(0))
            bad_delim_match = re.search(r'[^\d' + re.escape(delim) + ']', new_string)
            if bad_delim_match:
                bad_delim = bad_delim_match.group(0)
                k = new_string.index(bad_delim)
                error_messages.append(f"{delim} expected but {bad_delim} found at position {k}.")

            numbers = [int(n) for n in re.split(re.escape(delim), new_string) if int(n) <= 1000]
            if error_messages:
                raise Exception("\n".join(error_messages))
            return sum(numbers)

        numbers = [int(n) for n in re.split(delimiter, string) if int(n) <= 1000]

        if error_messages:
            raise Exception("\n".join(error_messages))

        return sum(numbers)
