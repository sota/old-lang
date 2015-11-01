
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
    return SastPair.from_pylist(list(items))

def car(exp):
    return exp.car

def cdr(exp):
    return exp.cdr

def caar(exp):
    return car(car(exp))

def cadr(exp):
    return car(cdr(exp))

def cdar(exp):
    return cdr(car(exp))

def cddr(exp):
    return cdr(cdr(exp))

def caaar(exp):
    car(car(car(exp)))

def caadr(exp):
    car(car(cdr(exp)))

def cadar(exp):
    car(cdr(car(exp)))

def caddr(exp):
    car(cdr(cdr(exp)))

def cdaar(exp):
    cdr(car(car(exp)))

def cdadr(exp):
    cdr(car(cdr(exp)))

def cddar(exp):
    cdr(cdr(car(exp)))

def cdddr(exp):
    cdr(cdr(cdr(exp)))

def caaaar(exp):
    car(car(car(car(exp))))

def caaadr(exp):
    car(car(car(cdr(exp))))

def caadar(exp):
    car(car(cdr(car(exp))))

def caaddr(exp):
    car(car(cdr(cdr(exp))))

def cadaar(exp):
    car(cdr(car(car(exp))))

def cadadr(exp):
    car(cdr(car(cdr(exp))))

def caddar(exp):
    car(cdr(cdr(car(exp))))

def cadddr(exp):
    car(cdr(cdr(cdr(exp))))

def cdaaar(exp):
    cdr(car(car(car(exp))))

def cdaadr(exp):
    cdr(car(car(cdr(exp))))

def cdadar(exp):
    cdr(car(cdr(car(exp))))

def cdaddr(exp):
    cdr(car(cdr(cdr(exp))))

def cddaar(exp):
    cdr(cdr(car(car(exp))))

def cddadr(exp):
    cdr(cdr(car(cdr(exp))))

def cdddar(exp):
    cdr(cdr(cdr(car(exp))))

def cddddr(exp):
    cdr(cdr(cdr(cdr(exp))))

def set_car(exp, value):
    exp.car = value

def set_cdr(exp, value):
    exp.cdr = value

class SastTailCall(Exception):
    def __init__(self, env, exp):
        self.env = env
        self.exp = exp
    def payload(self):
        return self.env, self.exp

class SastExp(object):

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

    def to_str(self):
        raise NotImplementedError

    def to_string(self):
        raise NotImplementedError

    def hashfn(self):
        return compute_identity_hash(self)

    def Eval(self, env):
        return self

    def EvalArgs(self, exp):
        return exp

    def Call(self, env, exp):
        return self

    def default(self):
        raise NotImplementedError

class SastUndefined(SastExp):

    def __init__(self):
        self.undefined = "<undefined>"

    def to_str(self):
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

class SastObject(SastExp):

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
            cls._true = SastExp.__new__(cls)
        return cls._true

    def __init__(self, value):
        assert value

    def default(self):
        return true

    def to_str(self):
        return "true"

    def to_string(self):
        return SastString("true")

true = SastTrue(True)

class SastFalse(SastBool):

    _false = None
    def __new__(cls, value):
        if cls._false is None:
            cls._false = SastExp.__new__(cls)
        return cls._false

    def __init__(self, value):
        assert not value

    def default(self):
        return false

    def to_str(self):
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

    def to_str(self):
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

    def to_str(self):
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

    def to_str(self):
        return self.symbol

    def hashfn(self):
        return _hash_string(self.symbol) or 0

    def Eval(self, env):
        return env.Get(self)

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
Print       = SastSymbol("print")

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

    def to_str(self):
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

    def to_str(self):
        result = ""
        exp = self
        while True:
            result += exp.car.to_str()
            if exp.cdr.is_nil():
                break
            elif not exp.cdr.is_pair():
                result += " . " + exp.cdr.to_str()
                break
            result += " "
            exp = exp.cdr
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
    def from_pylist(pylist):
        pylist.reverse()
        pair = nil
        for item in pylist:
            pair = SastPair(item, pair)
        return pair

    def is_tagged(self, tag=None):
        if self.is_pair():
            if self.car.is_symbol():
                if self.cdr.is_pair():
                    if tag and self.car != tag:
                        return False
                    return True
        return False

    def Eval(self, env):
        func = car(self).Eval(env)
        args = func.EvalArgs(cdr(self))
        return func.Call(env, args)

class SastQuote(SastPair):

    def __init__(self, cdr):
        self.car = Quote
        self.cdr = cdr

    def to_str(self):
        return "'" + self.cdr.to_str()

    def hashfn(self):
        return 1

    def Eval(self, env):
        return self.cdr

def hashfn(exp):
    return exp.hashfn()

def hasheq(exp1, exp2):
    return exp1.hashfn() == exp2.hashfn()

class SastDict(SastObject):

    def __init__(self):
        super(SastDict, self).__init__()

    def default(self):
        return emptydict

    def to_str(self):
        result = []
        for key, value in self.slots.iteritems():
            result += [key.to_str() + ": " + value.to_str()]
        return "{ " + " ".join(result) + " }"

    def Set(self, key, value):
        return self.insert(key, value)

    def Get(self, key, default=undefined):
        return self.lookup(key, default)

    def rem(self, key):
        return self.remove(key)

emptydict = SastDict()

class SastBlock(SastPair):

    def __init__(self, stmts):
        assert isinstance(stmts, SastPair)
        self.car = Block
        self.cdr = stmts

    def to_str(self):
        result = self.cdr.to_str()
        if len(result) > 2:
            return "{" + result + "}"
        raise SastBlockLengthError

    def Eval(self, env):
        exp = cdr(self)
        while exp.length() > 1:
            car(exp).Eval(env)
            exp = cdr(exp)
        exp = car(exp)
        raise SastTailCall(env, exp)

class SastFunc(SastExp):

    def __init__(self, env, formals):
        self.env = env
        self.formals = formals
        self.idx = 0

    def EvalArgs(self, exp):
        args = exp.to_pylist()
        return SastPair.from_pylist(args[:self.idx] + [arg.Eval(self.env) for arg in args[self.idx:]])

    def Eval(self, env):
        raise NotImplementedError

class SastBuiltin(SastFunc):

    def __init__(self, env):
        super(SastBuiltin, self).__init__(env, None)

    def to_str(self):
        return "<builtin " + self.__class__.__name__ + ">"

    def call(self, env, exp):
        raise NotImplementedError

    def Call(self, env, exp):
        return self.call(env, exp)

class SastLambda(SastFunc):

    def __init__(self, env, formals, block):
        super(SastLambda, self).__init__(env, formals)
        self.block = block

