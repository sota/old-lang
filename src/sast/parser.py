import os

from rpython.rtyper.lltypesystem import lltype

from sast.tokens import Token
from sast.lexer import Lexer
from sast.expressions import *
from sast.environment import *

from version import SOTA_VERSION

REPL_USAGE = '''
sota: state of the art
version: %s
exit: ctrl+c | ctrl+d, return
welcome to the sota repl!
''' % SOTA_VERSION

def stdin_readline():
    line = ''
    char = os.read(0, 1)
    while char not in ('', '\n'):
        line += char
        char = os.read(0, 1)
    return line

class MissingToken(Exception):
    pass

class ImproperListNotFollowedByRightParen(Exception):
    pass

class Parser(object):

    def __init__(self, lexer):
        self.lexer = lexer

    def parse(self, source):
        exitcode = 0
        self._print(self._eval(self._read(source)))
        return exitcode

    def repl(self):
        exitcode = 0
        print REPL_USAGE
        prompt = "sota> "
        while True:
            os.write(1, prompt)
            source = None
            try:
                source = stdin_readline()
                if not source:
                    print
                    break
                self._print(self._eval(self._read(source)))
            except KeyboardInterrupt:
                break
            except EOFError:
                break

        return exitcode

    def _read_pair(self):
        token, distance, _ = self.lexer.lookahead1()
        if not token:
            raise MissingToken
        if token.is_name(")"):
            self.lexer.consume()
            return nil
        car = self._read()
        token, _, _ = self.lexer.lookahead1()
        assert token
        if token.is_name('.'):
            self.lexer.consume()
            cdr = self._read()
            if not self.lexer.consume(')'):
                raise ImproperListNotFollowedByRightParen
        else:
            cdr = self._read_pair()
        return SastPair(car, cdr)

    def _read(self, source=None):
        if source:
            self.lexer.scan(source)
        token = self.lexer.consume()
        if token.is_name("sym"):
            if token.value == "true":
                return true
            elif token.value == "false":
                return false
            if token.value in ("'", "quote"):
                return SastQuote(self._read())
            return SastSymbol(token.value)
        elif token.is_name("str"):
            return SastString(token.value)
        elif token.is_name("num"):
            return SastFixnum(int(token.value))
        elif token.is_name("("):
            return self._read_pair()
        return SastUndefined()

    def _eval(self, expr):
        return expr.eval(Env)

    def _print(self, expr):
        if expr and isinstance(expr, SastExpr):
            print expr.to_format()

