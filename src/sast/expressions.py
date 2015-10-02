
from rpython.rlib.objectmodel import compute_identity_hash
#from rpython.rlib.objectmodel import _hash_float, _hash_string, specialize
from rpython.rlib.rarithmetic import LONG_BIT, intmask, ovfcheck
from rpython.rlib.objectmodel import import_from_mixin, r_ordereddict

from sast.exceptions import *

def _hash_string(string):
    # Cribbed from RPython's _hash_string.
    length = len(string)
    if length == 0:
        return -1
    x = ord(string[0]) << 7
    i = 0
    while i < length:
        x = intmask((1000003 * x) ^ ord(string[i]))
        i += 1
    x ^= length
    return intmask(x)

def _cons(car, cdr):
    return SastPair(car, cdr)

def _list(*items):
    return SastPair.from_pylist(*items)

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

    def is_block(self):
        return isinstance(self, SastBlock)

    def is_lambda(self):
        return isinstance(self, SastLambda)

    def is_builtin(self):
        return isinstance(self, SastBuiltin)

    def pystr(self):
        raise NotImplementedError

    def to_string(self):
        raise NotImplementedError

    def hashfn(self):
        return compute_identity_hash(self)

    def eval(self, env):
        return self

    def call(self, env, exprs):
        return self

    def default(self):
        raise NotImplementedError

class SastUndefined(SastExpr):

    def __init__(self):
        self.undefined = "<undefined>"

    def pystr(self):
        return self.undefined

    def to_string(self):
        return self.undefined

    def add(self, right):
        return undefined

    def sub(self, right):
        return undefined

    def mul(self, right):
        return undefined

    def div(self, right):
        return undefined

undefined = SastUndefined()

class SastObject(SastExpr):

    def __init__(self):
        self.slots = r_ordereddict(hasheq, hashfn)

    def default(self):
        return None

    def insert(self, key, value):
        self.slots[key] = value
        return value

    def lookup(self, key, default=undefined):
        value = self.slots.get(key, default)
        if value is None:
            if default is None:
                raise Exception
        return value

    def remove(self, key):
        del self.slots[key]

class SastAtom(SastObject):

    def __init__(self, value):
        assert isinstance(value, str)
        self.value = value

    def is_args(self):
        if self.is_symbol():
            if len(self.value) > 1:
                f, s = self.value[0:1]
                return f == "*" and s != "*"
        return False

    def is_kwargs(self):
        if self.is_symbol():
            if len(self.value) > 2:
                f, s = self.value[0:1]
                return f == "*" and s == "*"
        return False

    def default(self):
        raise NotImplementedError

class SastBool(SastAtom):

    def __new__(cls, value):
        if value:
            return true
        else:
            return false

    def __init__(self, value):
        pass

    def default(self):
        return false

class SastTrue(SastBool):

    _true = None
    def __new__(cls, value):
        if cls._true is None:
            cls._true = SastExpr.__new__(cls)
        return cls._true

    def __init__(self, value):
        assert value

    def default(self):
        return true

    def pystr(self):
        return "true"

    def to_string(self):
        return SastString("true")

true = SastTrue(True)

class SastFalse(SastBool):

    _false = None
    def __new__(cls, value):
        if cls._false is None:
            cls._false = SastExpr.__new__(cls)
        return cls._false

    def __init__(self, value):
        assert not value

    def default(self):
        return false

    def pystr(self):
        return "false"

    def to_string(self):
        return SastString("false")

false = SastFalse(False)

class SastFixnum(SastAtom):

    def __init__(self, value):
        assert isinstance(value, int)
        self.fixnum = value

    def default(self):
        return SastFixnum.zero

    def to_string(self):
        return SastString(str(self.fixnum))

    def pystr(self):
        return str(self.fixnum)

    def hashfn(self):
        return self.fixnum

    def add(self, right):
        return right.add_fixnum(self)

    def add_fixnum(self, left):
        return SastFixnum(left.fixnum + self.fixnum)

    def add_string(self, left):
        return SastString(left.string + str(self.fixnum))

    def sub(self, right):
        return right.sub_fixnum(self)

    def sub_fixnum(self, left):
        return SastFixnum(left.fixnum - self.fixnum)

    def mul(self, right):
        return right.mul_fixnum(self)

    def mul_fixnum(self, left):
        return SastFixnum(left.fixnum * self.fixnum)

    def mul_string(self, left):
        result = ""
        for x in xrange(self.fixnum):
            result += left.string
        return SastString(result)

    def div(self, right):
        return right.div_fixnum(self)

    def div_string(self, left):
        return left.div(self.to_string())

    def div_fixnum(self, left):
        return SastFixnum(left.fixnum / self.fixnum)

SastFixnum.zero = SastFixnum(0)

class SastString(SastAtom):

    def __init__(self, value):
        assert isinstance(value, str)
        self.string = value

    def default(self):
        return SastString.empty

    def to_string(self):
        return self

    def pystr(self):
        return '"' + self.string + '"'

    def hashfn(self):
        return _hash_string('"' + self.string + '"')

    def add(self, right):
        return right.add_string(self)

    def add_string(self, left):
        return SastString(left.string + self.string)

    def add_fixnum(self, left):
        return SastString(str(left.fixnum) + self.string)

    def mul(self, right):
        return right.mul_string(self)

    def mul_fixnum(self, left):
        return left.mul_string(self)

    def div(self, right):
        return right.div_string(self)

    def div_string(self, left):
        return SastString(left.string + "/" + self.string)

    def div_fixnum(self, left):
        return left.to_string().div(self)

SastString.empty = SastString("")

class SastSymbol(SastAtom):

    Table = {}

    def __new__(cls, value):
        symbol = cls.Table.get(value, None)
        if not symbol:
            cls.Table[value] = symbol = super(SastSymbol, cls).__new__(cls, value)
        return symbol

    def __init__(self, value):
        assert isinstance(value, str)
        self.symbol = value

    def default(self):
        raise NotImplementedError

    def to_string(self):
        return SastString(self.symbol)

    def pystr(self):
        return self.symbol

    def hashfn(self):
        return _hash_string(self.symbol) or 0

    def eval(self, env):
        return env.get(self)

Cons        = SastSymbol("cons")
Assign      = SastSymbol("=")
Lambda      = SastSymbol("->")
Quote       = SastSymbol("'")
Block       = SastSymbol("block")
List        = SastSymbol("list")
As          = SastSymbol("as")
If          = SastSymbol("if")
In          = SastSymbol("in")
Is          = SastSymbol("is")
Or          = SastSymbol("or")
And         = SastSymbol("and")
Range       = SastSymbol("..")
Ellipses    = SastSymbol("...")
Add         = SastSymbol("+")
Sub         = SastSymbol("-")
Mul         = SastSymbol("*")
Div         = SastSymbol("/")
AddAssign   = SastSymbol("+=")
SubAssign   = SastSymbol("-=")
MulAssign   = SastSymbol("*=")
DivAssign   = SastSymbol("/=")

class SastList(SastObject):

    def __init__(self):
        pass

    def length(self):
        raise NotImplementedError

class SastNil(SastList):

    _nil = None

    def __new__(cls):
        if not cls._nil:
            cls._nil = super(SastNil, cls).__new__(cls)
        return cls._nil

    def __init__(self):
        self.nil = '()'

    def length(self):
        return 0

    def pystr(self):
        return self.nil

nil = SastNil()

class SastPair(SastList):

    def __init__(self, car=nil, cdr=nil):
        self.car = car
        self.cdr = cdr

    def length(self):
        result = 0
        if self.car:
            result += 1
        if self.cdr:
            result += self.cdr.length()
        return result

    def default(self):
        return nil

    def is_args(self):
        return False

    def is_kwargs(self):
        return False

    def pystr(self):
        result = ""
        expr = self
        while True:
            result += expr.car.pystr()
            if expr.cdr.is_nil():
                break
            elif not expr.cdr.is_pair():
                result += " . " + expr.cdr.pystr()
                break
            result += " "
            expr = expr.cdr
        return "(" + result + ")"

    def to_pylist(self):
        pylist = []
        pair = self
        while pair != nil:
            if not pair.is_list():
                raise SastWrongArgType(pair, "list")
            pylist.append(pair.car)
            pair = pair.cdr
        return pylist

    @staticmethod
    def from_pylist(*args):
        pylist = list(args)
        pylist.reverse()
        cdr = nil
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
        func = self.car.eval(env)
        return func.call(env, self.cdr)

class SastQuote(SastPair):

    def __init__(self, cdr):
        self.car = Quote
        self.cdr = cdr

    def pystr(self):
        return "'" + self.cdr.pystr()

    def hashfn(self):
        return 1

    def eval(self, env):
        return self.cdr

def hashfn(expr):
    return expr.hashfn()

def hasheq(expr1, expr2):
    return expr1.hashfn() == expr2.hashfn()

class SastDict(SastObject):

    def __init__(self):
        super(SastDict, self).__init__()

    def default(self):
        return emptydict

    def pystr(self):
        result = []
        for key, value in self.slots.iteritems():
            result += [key.pystr() + ": " + value.pystr()]
        return "{" + " ".join(result) + "}"

    def put(self, key, value):
        return self.insert(key, value)

    def get(self, key, default=undefined):
        return self.lookup(key, default)

    def rem(self, key):
        return self.remove(key)

emptydict = SastDict()

class SastBlock(SastPair):

    def __init__(self, env, stmts):
        assert isinstance(stmts, SastPair)
        self.env = env
        self.car = Block
        self.cdr = stmts

    def pystr(self):
        result = self.cdr.pystr()
        if len(result) > 2:
            return "{" + result + "}"
        raise Exception("SastBlock.pystr: len of result not > 2")

class SastLambda(SastPair):

    def __init__(self, definition):
        self.car = Lambda
        self.cdr = definition

    @property
    def formals(self):
        return cadr(self)

    @property
    def block(self):
        return caddr(self)

class SastBuiltin(SastExpr):

    def __init__(self, symbol, formals, call):
        self.symbol = symbol
        self.formals = formals
        self._call = call

    @property
    def block(self):
        raise NotImplementedError

    def pystr(self):
        result = SastPair(self.symbol, self.formals).pystr()
        return "<builtin " + result + ">"

    def call(self, env, expr):
        return self._call(env, expr)

