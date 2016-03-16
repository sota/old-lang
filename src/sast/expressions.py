
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
        return "'false"

true = SastBoolean(True)
false = SastBoolean(False)

class SastSymbol(SastObject):
    def __init__(self, value):
        self.value = str(value)
    def repr(self):
        return self.value

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

