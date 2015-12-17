#!/usr/bin/python3

import re
from collections import namedtuple

text = """for i in 1 to 5:
    my-var = print(1+3*i);
    return my-var;
    endfor"""

KEYWORD_RE = r"(?P<KEYWORD>for|in|to|endfor|return)"
VAR_RE = r"(?P<VAR>[a-zA-Z][_a-zA-Z0-9-]*)"
NUM_RE = r"(?P<NUM>[0-9]+)"
SYM_RE = r"(?P<SYM>[;:()])"
OP_RE = r"(?P<OP>[+*=])"
WS_RE = r"(?P<WS>\s+)"

MASTER_RE = re.compile("|".join([KEYWORD_RE, VAR_RE, NUM_RE, SYM_RE, OP_RE, WS_RE]))


TOKEN = namedtuple("TOKEN", ["token", "text"])

def get_token(text: str, re):
    scanner = re.scanner(text)
    for m in iter(scanner.match, None):
        yield TOKEN(m.lastgroup, m.group())

print("Parsing", text)
print()

for i in get_token(text, MASTER_RE):
    if i.token != "WS":
        print(i.token, ' -> ', i.text)

