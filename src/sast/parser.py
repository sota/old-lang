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

    def Parse(self, source):
        exitcode = 0
        try:
            self.Eval(self.Read(source))
        except Exception as ex:
            raise
        return exitcode

    def Repl(self):
        exitcode = 0
        print REPL_USAGE
        prompt = "sota> "
        while True:
            os.write(1, prompt)
            source = None
            try:
                source = stdin_readline()
                if not source:
                    print "goodbye!"
                    break
                code = self.Read(source)
                exp = self.Eval(code)
                if exp is None:
                    print "goodbye!"
                    break
                self.Print(exp)
            except KeyboardInterrupt:
                break
            except EOFError:
                break
        return exitcode

    def ReadPair(self):
        token, _, _ = self.lexer.lookahead1()
        if not token:
            raise MissingToken
        if token.is_name(")"):
            self.lexer.consume()
            return nil
        car = self.Read()
        token, _, _ = self.lexer.lookahead1()
        assert token
        if token.is_name("."):
            self.lexer.consume()
            cdr = self.Read()
            if not self.lexer.consume(")"):
                raise ImproperListNotFollowedByRightParen
        else:
            cdr = self.ReadPair()
        return SastPair(car, cdr)

    def ReadBlock(self):
        token, _, _ = self.lexer.lookahead1()
        if not token:
            raise MissingToken
        if token.is_name("}"):
            self.lexer.consume()
            return nil
        car = self.Read()
        token, _, _ = self.lexer.lookahead1()
        assert token
        cdr = self.ReadBlock()
        return SastPair(car, cdr)

    def Read(self, source=None):
        if source:
            self.lexer.scan(source)
        token = self.lexer.consume()
        if token.is_name("sym"):
            if token.value == "true":
                return true
            elif token.value == "false":
                return false
            if token.value in ("'", "quote"):
                return SastQuote(self.Read())
            return SastSymbol(token.value)
        elif token.is_name("str"):
            return SastString(token.value)
        elif token.is_name("num"):
            return SastFixnum(int(token.value))
        elif token.is_name("("):
            return self.ReadPair()
        elif token.is_name("{"):
            stmts = self.ReadBlock()
            return SastBlock(stmts)
        return SastUndefined()

    def Eval(self, exp):
        return exp.Eval(Env)

    def Print(self, exp):
        if exp and isinstance(exp, SastExp):
            print exp.to_str()

