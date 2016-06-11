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
        env = Env
        if os.path.isfile(source):
            source = open(source).read()
        else:
            source = "(print " + source + ")"
        try:
            code = self.Read(source)
            self.Eval(code, env)
        except Exception as ex:
            raise
        return exitcode

    def Repl(self):
        exitcode = 0
        env = Env
        farewell = "so, ta-ta for now!"
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
                exp = self.Eval(code, env)
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
            elif token.value == "=":
                return Assign
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

    def Eval(self, exp, env):
        while True:
            try:
                if exp.is_symbol():
                    return env.Get(exp)
                elif exp.is_atom():
                    return exp
                    return env.Get(exp)
                elif exp.is_quote():
                    return exp.cdr
                elif exp.is_tagged(Assign):
                    if exp.length() != 3:
                        raise SastSyntaxError
                    if not exp.car.is_symbol():
                        raise SastSyntaxError
                    key, value = exp.to_pylist()[1:]
                    return env.Set(key, self.Eval(value, env))
                elif exp.is_tagged(Block):
                    while exp.length() > 1:
                        self.Eval(exp.car, env)
                        exp = exp.cdr
                    raise SastTailCall(exp.car, env)
                else:
                    print 'didnt match anything'
                    print 'exp =', exp.to_str()
                return exp
            except SastTailCall as stc:
                exp, env = stc.payload()

    def Print(self, exp):
        if exp and isinstance(exp, SastExp):
            print exp.to_str()

