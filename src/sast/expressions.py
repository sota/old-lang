
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

class SastObject(SastExp):
    def __init__(self):
        self.od = r_ordereddict(hasheq, hashfn)

class SastUndefined(SastObject):
    def __init__(self):
        pass

