import os

from rpython.rtyper.lltypesystem import lltype

from sast.tokens import Token
from sast.lexer import Lexer
from sast.builtins import *
from sast.expressions import *
from sast.environment import *

from version import SOTA_VERSION

REPL_USAGE = '''
sota: state of the art
version: %s
exit: ctrl+c | ctrl+d, return
welcome to the sota repl!
''' % SOTA_VERSION

class MissingToken(Exception):
    pass

class ImproperListNotFollowedByRightParen(Exception):
    pass

class NestingError(Exception):
    pass

def get_input():
    text = ""
    nesting = 0
    while True:
        char = os.read(0, 1)
        text += char
        if char == '(':
            nesting += 1
        elif char == ')':
            nesting -= 1
        if char == '\n':
            if nesting == 0:
                break
            elif nesting < 0:
                raise NestingError
        elif char == '':
            raise EOFError
    return text

class Parser(object):

    def __init__(self, lexer):
        self.lexer = lexer

    def Parse(self, source):
        exitcode = 0
        if os.path.isfile(source):
            source = open(source).read()
        else:
            source = "(print " + source + ")"
        try:
            self.Eval(self.Read(source))
        except Exception as ex:
            raise
        return exitcode

    def Repl(self):
        exitcode = 0
        farewell = "sota tfn!"
        print REPL_USAGE
        prompt = "sota> "
        while True:
            os.write(1, prompt)
            source = None
            try:
                source = get_input()
                if source == '\n':
                    continue
                code = self.Read(source)
                exp = self.Eval(code)
                if exp is None:
                    print farewell
                    break
                self.Print(exp)
            except KeyboardInterrupt:
                break
            except EOFError:
                print farewell
                break
        return exitcode

    def Read(self, source=None):
        if source:
            self.lexer.scan(source)
        token = self.lexer.consume()
        print 'token =', token.to_str()
        if token.is_name("sym"):
            if token.value == "true":
                return true
            elif token.value == "false":
                return false
#            if token.value in ("'", "quote"):
#                return SastQuote(self.Read())
            return SastSymbol(token.value)
        elif token.is_name("str"):
            return SastString(token.value)
        elif token.is_name("num"):
            return SastFixnum(int(token.value))
#        elif token.is_name("("):
#            return self.ReadPair()
        return SastUndefined()

    def Eval(self, exp):
        return exp


    def Print(self, exp):
        if exp and isinstance(exp, SastExp):
            print exp.repr()
