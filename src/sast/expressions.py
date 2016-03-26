
from rpython.rlib.objectmodel import compute_identity_hash
from rpython.rlib.rarithmetic import LONG_BIT, intmask, ovfcheck
from rpython.rlib.objectmodel import import_from_mixin, r_ordereddict

from sast.exceptions import *

def hashfn(exp):
    return exp.hashfn()

def hasheq(exp1, exp2):
    return exp1.hashfn() == exp2.hashfn()

class SastExp(object):

    def __init__(self):
        self.is_self_eval = False

    def hashfn(self):
        return compute_identity_hash(self)

    def to_repr(self):
        return 'not-implemented'

    def is_a(self, kind, value=None):
        result = isinstance(self, kind)
        if value:
            return self == value
        return result

    def is_tagged(self, sym):
        return False

class SastObject(SastExp):

    def __init__(self):
        self.slots = r_ordereddict(hasheq, hashfn)

class SastSelfEvalObject(SastObject):
    pass

class SastUndefined(SastSelfEvalObject):

    def __init__(self):
        pass

    def to_repr(self):
        return "<undefined>"

class SastBoolean(SastSelfEvalObject):

    def __init__(self, value):
        self.value = bool(value)

    def to_repr(self):
        if self.value:
            return "true"
        return "false"

true = SastBoolean(True)
false = SastBoolean(False)

class SastSymbol(SastObject):

    def __init__(self, value):
        self.value = str(value)

    def to_repr(self):
        return self.value

Cons        = SastSymbol("cons")
Assign      = SastSymbol("=")
Lambda      = SastSymbol("->")
Quote       = SastSymbol("quote")
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

class SastString(SastSelfEvalObject):

    def __init__(self, value):
        self.value = str(value)

    def to_repr(self):
        return '"' + self.value + '"'

class SastFixnum(SastSelfEvalObject):

    def __init__(self, value):
        self.value = int(value)

    def to_repr(self):
        return str(self.value)

class SastList(SastObject):

    def __init__(self):
        pass

    def length(self):
        raise NotImplementedError

class SastNil(SastList):

    _value = None
    def __new__(cls):
        if not cls._value:
            cls._value = super(SastNil, cls).__new__(cls)
        return cls._value

    def __init__(self):
        self.value = '()'

    def length(self):
        return 0

    def to_repr(self):
        return self.value

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

    def to_repr(self):
        result = ""
        exp = self
        while True:
            result += exp.car.to_repr()
            if exp.cdr.is_a(SastNil):
                break
            elif not exp.cdr.is_a(SastPair):
                result += " . " + exp.cdr.to_repr()
                break
            result += " "
            exp = exp.cdr
        return "(" + result + ")"

    def is_tagged(self, sym):
        if self.car != nil:
            return self.car == sym
        return False

    def to_pylist(self):
        pylist = []
        pair = self
        while pair != nil:
            if not pair.is_a(SastList):
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

