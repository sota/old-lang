
import operator as op
from sast.exceptions import *

def cons(car, cdr):
    return SastPair(car, cdr)

def car(expr):
    return expr.car

def cdr(expr):
    return expr.cdr

def caar(expr):
    return car(car(expr))

def cadr(expr):
    return car(cdr(expr))

def cdar(expr):
    return cdr(car(expr))

def cddr(expr):
    return cdr(cdr(expr))

def caaar(expr):
    car(car(car(expr)))

def caadr(expr):
    car(car(cdr(expr)))

def cadar(expr):
    car(cdr(car(expr)))

def caddr(expr):
    car(cdr(cdr(expr)))

def cdaar(expr):
    cdr(car(car(expr)))

def cdadr(expr):
    cdr(car(cdr(expr)))

def cddar(expr):
    cdr(cdr(car(expr)))

def cdddr(expr):
    cdr(cdr(cdr(expr)))

def caaaar(expr):
    car(car(car(car(expr))))

def caaadr(expr):
    car(car(car(cdr(expr))))

def caadar(expr):
    car(car(cdr(car(expr))))

def caaddr(expr):
    car(car(cdr(cdr(expr))))

def cadaar(expr):
    car(cdr(car(car(expr))))

def cadadr(expr):
    car(cdr(car(cdr(expr))))

def caddar(expr):
    car(cdr(cdr(car(expr))))

def cadddr(expr):
    car(cdr(cdr(cdr(expr))))

def cdaaar(expr):
    cdr(car(car(car(expr))))

def cdaadr(expr):
    cdr(car(car(cdr(expr))))

def cdadar(expr):
    cdr(car(cdr(car(expr))))

def cdaddr(expr):
    cdr(car(cdr(cdr(expr))))

def cddaar(expr):
    cdr(cdr(car(car(expr))))

def cddadr(expr):
    cdr(cdr(car(cdr(expr))))

def cdddar(expr):
    cdr(cdr(cdr(car(expr))))

def cddddr(expr):
    cdr(cdr(cdr(cdr(expr))))

def set_car(expr, value):
    expr.car = value

def set_cdr(expr, value):
    expr.cdr = value

class SastExpr(object):

    def __init__(self):
        pass

    def is_undefined(self):
        return isinstance(self, SastUndefined)

    def is_atom(self):
        return isinstance(self, SastAtom)

    def is_bool(self):
        return isinstance(self, SastBool)

    def is_true(self):
        return isinstance(self, SastTrue)

    def is_false(self):
        return isinstance(self, SastFalse)

    def is_fixnum(self):
        return isinstance(self, SastFixnum)

    def is_string(self):
        return isinstance(self, SastString)

    def is_symbol(self):
        return isinstance(self, SastSymbol)

    def is_args(self):
        raise NotImplementedError

    def is_kwargs(self):
        raise NotImplementedError

    def is_list(self):
        return isinstance(self, SastList)

    def is_pair(self):
        return isinstance(self, SastPair)

    def is_nil(self):
        return isinstance(self, SastNil)

    def is_tagged(self, tag=None):
        return False

    def is_dict(self):
        return isinstance(self, SastDict)

    def is_lambda(self):
        return isinstance(self, SastLambda)

    def is_builtin(self):
        return isinstance(self, SastBuiltin)

    def to_format(self):
        raise NotImplementedError

    def eval(self, env):
        return self

    def call(self, env, exprs):
        return self

class SastAtom(SastExpr):

    def __init__(self, value):
        assert isinstance(value, str)
        self.value = value

    def to_format(self):
        return self.value

    def is_args(self):
        if self.is_symbol():
            if len(self.value) > 1:
                f, s = self.value[0:1]
                return f == '*' and s != '*'
        return False

    def is_kwargs(self):
        if self.is_symbol():
            if len(self.value) > 2:
                f, s = self.value[0:1]
                return f == '*' and s == '*'
        return False

class SastUndefined(SastAtom):

    def __init__(self):
        self.value = '<undefined>'

undefined_symbol = SastUndefined()

class SastBool(SastAtom):

    def __new__(cls, value):
        if value:
            return true
        else:
            return false

    def __init__(self, value):
        pass

class SastTrue(SastBool):

    _true = None
    def __new__(cls, value):
        if cls._true is None:
            cls._true = SastExpr.__new__(cls)
        return cls._true

    def __init__(self, value):
        assert value
        self.value = 'true'

true = SastTrue(True)

class SastFalse(SastBool):

    _false = None
    def __new__(cls, value):
        if cls._false is None:
            cls._false = SastExpr.__new__(cls)
        return cls._false

    def __init__(self, value):
        assert not value
        self.value = 'false'

false = SastFalse(False)

class SastFixnum(SastAtom):

    def __init__(self, value):
        assert isinstance(value, str)
        self.value = value

class SastString(SastAtom):

    def __init__(self, value):
        assert isinstance(value, str)
        self.value = value

    def to_format(self):
        return '"' + self.value + '"'

class SastSymbol(SastAtom):

    Table = {}

    def __new__(cls, value):
        symbol = cls.Table.get(value, None)
        if not symbol:
            cls.Table[value] = symbol = super(SastSymbol, cls).__new__(cls, value)
        return symbol

    def __init__(self, value):
        assert isinstance(value, str)
        self.value = value

    def eval(self, env):
        return env.lookup(self)

#class SastArgs(SastSymbol):
#
#    def __new__(cls, value):
#        symbol = cls.Table.get(value, None)
#        if not symbol:
#            cls.Table[value] = symbol = super(SastArgs, cls).__new__(cls, value)
#        return symbol
#
#    def __init__(self, value):
#        super(SastArgs, self).__init__(value)
#
#class SastKwargs(SastSymbol):
#
#    def __new__(cls, value):
#        symbol = cls.Table.get(value, None)
#        if not symbol:
#            cls.Table[value] = symbol = super(SastKwargs, cls).__new__(cls, value)
#        return symbol
#
#    def __init__(self, value):
#        super(SastKwargs, self).__init__(value)

assign_symbol   = SastSymbol("=")
lambda_symbol   = SastSymbol("->")
quote_symbol    = SastSymbol("'")
block_symbol    = SastSymbol("block")
list_symbol     = SastSymbol("list")
as_symbol       = SastSymbol("as")
if_symbol       = SastSymbol("if")
in_symbol       = SastSymbol("in")
is_symbol       = SastSymbol("is")
or_symbol       = SastSymbol("or")
and_symbol      = SastSymbol("and")
range_symbol    = SastSymbol("..")
ellipses_symbol = SastSymbol("...")

class SastList(SastExpr):

    def __init__(self):
        pass

class SastNil(SastList):

    _nil = None

    def __new__(cls):
        if not cls._nil:
            cls._nil = super(SastNil, cls).__new__(cls)
        return cls._nil

    def __init__(self):
        self.value = '()'

    def __values__(self):
        return []

nil = SastNil()

class SastPair(SastList):

    def __init__(self, car=nil, cdr=nil):
        self.car = car
        self.cdr = cdr

    def is_args(self):
        return False

    def is_kwargs(self):
        return False

    def to_format(self):
        result = ''
        expr = self
        while True:
            result += expr.car.to_format()
            if expr.cdr.is_nil():
                break
            elif not expr.cdr.is_pair():
                result += ' . ' + expr.cdr.to_format()
                break
            result += ' '
            expr = expr.cdr
        return '(' + result + ')'

    def to_pylist(self):
        pylist = []
        pair = self
        while pair != nil:
            if not pair.is_pair():
                raise SastWrongArgType(pair, 'list')
            pylist.append(pair.car)
            pair = pair.cdr
        return pylist

    @staticmethod
    def from_pylist(*args, **kwargs):
        cdr = kwargs.pop('cdr', nil)
        pylist = list(args)
        pylist.reverse()
        for car in pylist:
            cdr = SastPair(car, cdr)
        return cdr

    def is_tagged(self, tag=None):
        if self.is_pair():
            if self.car.is_symbol():
                if self.cdr.is_pair():
                    if tag and self.car != tag:
                        return False
                    return True
        return False

    def eval(self, env):
        expr = self.car.eval(env)
        return expr.call(env, self.cdr)

class SastQuote(SastPair):

    def __init__(self, cdr):
        self.car = quote_symbol
        self.cdr = cdr

    def eval(self, env):
        return self.cdr

class SastDict(SastExpr):

    def __init__(self):
        self._dict = {}

    def lookup(self, symbol, default=undefined_symbol):
        value = self._dict.get(symbol.value, default)
        if value is None and default is None:
            raise Exception
        return value

    def assign(self, symbol, expr):
        self._dict[symbol.value] = expr

    def remove(self, symbol):
        del self._dict[symbol.value]

    def to_format(self):
        result = []
        for key, value in self._dict.iteritems():
            result += [key + ': ' + value.to_format()]
        return '{' + ' '.join(result) + '}'

class SastEnv(SastDict):
    pass

Env = SastEnv()
Env.assign(SastSymbol("a"), SastFixnum("1"))
Env.assign(SastSymbol("b"), SastFixnum("2"))
Env.assign(SastSymbol("c"), SastFixnum("3"))

class SastBlock(SastExpr):

    def __init__(self, env, stmts):
        assert isinstance(env, SastEnv)
        assert isinstance(stmts, SastPair)
        self.env = env
        self.stmts = stmts

    def to_format(self, *args, **kwargs):
        result = ' '.join([stmt.to_format() for stmt in self.stmts])
        return '{' + result[1:-1] + '}'

class SastLambda(SastExpr):

    def __init__(self, formals, block):
        self.formals = formals
        self.block = block

class SastBuiltin(SastLambda):

    def __init__(self, formals, call):
        super(SastBuiltin, self).__init__(formals, None)
        self._call = call

    def to_format(self):
        return '<builtin>'

    def call(self, env, exprs):
        return self._call(env, exprs.to_pylist())

class SastOp(SastLambda):

    def __init__(self, env, formals, block, name):
        super(SastOp, self).__init__(env, formals, block, name=name)

def assign(env, args):
    x, y = args
    env.assign(x, y)

assign_builtin = SastBuiltin(
    SastPair.from_pylist(SastSymbol("symbol"), SastSymbol("value")),
    assign)

Env.assign(SastSymbol("="), assign_builtin)
