#!/usr/bin/python3
#encoding: utf-8

"""Parse simple arithmetic expressions with variables.

expr := expr +/- term
term := factor *// factor
factor :=
"""

import re
from collections import namedtuple

PLUS = r"(?P<PLUS>\+)"
MINUS = r"(?P<MINUS>-)"
MULT = r"(?P<MULT>\*)"
DIV = r"(?P<DIV>/)"
NUM = r"(?P<NUM>[0-9]+)"
VAR = r"(?P<VAR>[a-zA-Z][_a-zA-Z0-9]*)"
EQ = r"(?P<EQ>=)"
SEMICOL = r"(?P<SEMICOL>;)"
LPAR = r"(?P<LPAR>\()"
RPAR = r"(?P<RPAR>\))"
WS = r"(?P<WS>\s+)"

expr_pat = re.compile("|".join([PLUS,MINUS,MULT,DIV,NUM,VAR,EQ,SEMICOL,LPAR,RPAR,WS]))

Token = namedtuple('Token', ['tok', 'val'])

def tokenizer(text, pat, skip_sw=True):
    scanner = pat.scanner(text)
    for m in iter(scanner.match, None):
        tok = Token(m.lastgroup, m.group())
        if not skip_sw or tok.tok != 'WS':
            yield tok

test_expr = r"a=1+3*(4-5*(2+3)); b=a+3;"
tokens = list(tokenizer(test_expr, expr_pat))

print(tokens)

class ExpressionEvaluator():

    def parse(self, expr):
        self.tok = None
        self.nexttok = None
        self.expr = expr
        self.lexer = tokenizer(self.expr, expr_pat)
        return self.expr_parse()

    def _accept(self, tok):
        if self.tok.tok == tok:
            self.tok = self.nexttok
            self.nexttok = next(self.lexer)
            return self.tok.val

    def _expect(self, tok):
        self.tok = next(self.lexer)
        self.toktok = next(self.lexer)
        if self.tok.tok == tok:
            return self._accept(tok)
        else:
            raise SyntaxError("Expecting a token: {}".format(tok.tok))

    def expr_parse(self):
        expr_val = self.term_parse()

        if self._accept('PLUS'):
            expr_val += self.term_parse()
            return expr_val
        if self._accept('MINUS'):
            expr_val -= self.term_parse()
            return expr_val

    def term_parse(self):
        term_val = self.factor_parse()

        if self._accept('MULT'):
            term_val *= self.factor_parse()
            return term_val
        if self._accept('DIV'):
            term_val -= self.factor_parse()
            return term_val

    def factor_parse(self):
        return self._expect('NUM')

parser = ExpressionEvaluator()
print(parser.parse("1+2"))


