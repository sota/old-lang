
from rpython.rlib.objectmodel import compute_identity_hash
from rpython.rlib.rarithmetic import LONG_BIT, intmask, ovfcheck
from rpython.rlib.objectmodel import import_from_mixin, r_ordereddict

from sast.exceptions import *


class SastExp(object):
    pass

class SastUndefined(SastExp):
    pass

