#!/usr/bin/python3

import sys

def sub(text):
    class safedict(dict):
        def __missing__(self, key):
            return "{" + str(key) + "}"

    return text.format_map(safedict(sys._getframe(1).f_locals))


n = 5
name = "Hello"

print(sub("{n} is here. Hello {name} even if it is not here {d}"))

text = "Another try with {n} and {name}, though unsafe with missing keys."
print(text.format_map(vars()))

