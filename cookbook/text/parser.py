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
VAR = r"(?P<VAR>[_a-zA-Z][_a-zA-Z0-9]*)"
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

#test_expr = r"a=1+3*(4-5*(2+3)); b=a+3;"
#tokens = list(tokenizer(test_expr, expr_pat))
#print(tokens)


class ExpressionEvaluator():
    """Parser for simple arithmetic expressions:
    prog:=stm+
    stm:=; | VAR; | VAR=expr; | expr;
    expr:= term {(+|-)term}*;
    term:= factor {(*|/)factor}*
    factor:= NUM | VAR | (expr)
    """
    def parse(self, expr):
        self.tok = None
        self.nexttok = None
        self.nextnexttok = None
        self.expr = expr
        self.scope = '_'
        self.symtab = {}
        self.symtab[self.scope] = {}
        self.lexer = tokenizer(self.expr, expr_pat)
        self._advance()
        return self.prog_parse()

    def _advance(self):
        self.tok, self.nexttok, self.nextnexttok = self.nexttok, self.nextnexttok, next(self.lexer, None)
        print("tok: {}, nexttok: {}".format(self.tok.tok if self.tok else 'None', self.nexttok.tok if self.nexttok else 'None'))

    def _accept(self, tok):
        if self.nexttok and self.nexttok.tok == tok:
            self._advance()
            return True
        return False

    def _expect(self, tok):
        if not self._accept(tok):
            raise SyntaxError("Expecting a token: {}".format(tok))

    def _get_var(self, var):
        if var in self.symtab[self.scope]:
            return self.symtab[self.scope][var]
        else:
            raise SyntaxError("Unknown variable: " + var)

    def _put_var(self, var, val):
        self.symtab[self.scope][var] = int(val)

    def prog_parse(self):
        while self.stm_parse():
            print('Statement')
            pass

    def stm_parse(self):
        if self._accept('SEMICOL'):
            print("Empty statement detected")
            return True
        elif self.nexttok is not None:
            # Perform LA-1
            print("LA-1 result: ", self.nextnexttok.tok)
            if self.nextnexttok.tok == 'EQ':
                # Assignment statement
                print("Assignment statement detected")
                self._expect('VAR')
                var = self.tok.val
                self._expect('EQ')
                exprval = self.expr_parse()
                self._put_var(var, exprval)
                self._expect('SEMICOL')
                return True
            elif self.nextnexttok.tok == 'SEMICOL':
                print("Print var statement detected")
                self._expect('VAR')
                var = self.tok.val
                val = self._get_var(var)
                print("{} = {}".format(var, val))
                self._expect('SEMICOL')
                return True
            else:
                print("Expression statement detected")
                exprval = self.expr_parse()
                self._put_var('_', exprval)
                self._expect('SEMICOL')
                return True
        else:
            return False

    def expr_parse(self):
        expr_val = self.term_parse()

        while self._accept('MINUS') or self._accept('PLUS'):
            tok = self.tok.tok
            op = self.term_parse()
            if tok == 'PLUS':
                expr_val += op
            elif tok == 'MINUS':
                expr_val -= op

        return expr_val

    def term_parse(self):
        term_val = self.factor_parse()

        while self._accept('MULT') or self._accept('DIV'):
            tok = self.tok.tok
            op = self.factor_parse()
            if tok == 'MULT':
                term_val *= op
            elif tok == 'DIV':
                term_val /= op

        return term_val

    def factor_parse(self):
        if self._accept('NUM'):
            return int(self.tok.val)
        elif self._accept('VAR'):
            var = self.tok.val
            if var in self.symtab[self.scope]:
                return self.symtab[self.scope][var]
            else:
                raise SyntaxError("Unknown variable: {}".format(var))
        elif self._accept('LPAR'):
            expr = self.expr_parse()
            self._expect('RPAR')
            return expr
        else:
            raise SyntaxError("Expecting NUM or LPAR")

parser = ExpressionEvaluator()
parser.parse("4*(5);;(1+3)+2*3;_+3+_+3;_;")


