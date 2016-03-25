
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
        pass

    def hashfn(self):
        return compute_identity_hash(self)

    def repr(self):
        return 'not-implemented'

    def isa(self, kind, value=None):
        result = isinstance(self, kind)
        if value:
            return self == value
        return result

    def istagged(self, sym):
        return False

class SastObject(SastExp):

    def __init__(self):
        self.slots = r_ordereddict(hasheq, hashfn)

class SastUndefined(SastObject):

    def __init__(self):
        pass

    def repr(self):
        return "<undefined>"

class SastBoolean(SastObject):

    def __init__(self, value):
        self.value = bool(value)

    def repr(self):
        if self.value:
            return "true"
        return "false"

true = SastBoolean(True)
false = SastBoolean(False)

class SastSymbol(SastObject):

    def __init__(self, value):
        self.value = str(value)

    def repr(self):
        return self.value

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

class SastString(SastObject):

    def __init__(self, value):
        self.value = str(value)

    def repr(self):
        return '"' + self.value + '"'

class SastFixnum(SastObject):

    def __init__(self, value):
        self.value = int(value)

    def repr(self):
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

    def repr(self):
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

    def repr(self):
        result = ""
        exp = self
        while True:
            result += exp.car.repr()
            if exp.cdr.isa(SastNil):
                break
            elif not exp.cdr.isa(SastPair):
                result += " . " + exp.cdr.repr()
                break
            result += " "
            exp = exp.cdr
        return "(" + result + ")"

    def istagged(self, sym):
        if self.car != nil:
            return self.cdr == sym
        return False

    def to_pylist(self):
        pylist = []
        pair = self
        while pair != nil:
            if not pair.isa(SastList):
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

