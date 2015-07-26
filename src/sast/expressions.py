
#pylint: disable=no-self-use,invalid-name

class SotaExpr(object):

    def to_string(self):
        return '<%r>' % (self,)

    def to_repr(self):
        return '#<unknown>'

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, self.to_string())

    def call(self, *args, **kwargs):
        print 'call: ', args, kwargs

class SotaUndefined(SotaExpr):
    def to_repr(self):
        return '#<undefined>'

class SotaBoolean(SotaExpr):
    def __new__(cls, value):
        if value:
            return true
        else:
            return false

class SotaTrue(SotaBoolean):
    _true = None
    def __new__(cls, value):
        if cls._true is None:
            cls._true = SotaExpr.__new__(cls)
        return cls._true

    def __init__(self, value):
        assert value

    def to_string(self):
        return 'true'

    to_repr = to_string

true = SotaTrue(True)

class SotaFalse(SotaBoolean):
    _false = None
    def __new__(cls, value):
        if cls._false is None:
            cls._false = SotaExpr.__new__(cls)
        return cls._false

    def __init__(self, value):
        assert not value

    def to_string(self):
        return 'false'

    to_repr = to_string

false = SotaFalse(False)

class SotaFixnum(SotaExpr):
    pass

class SotaString(SotaExpr):
    pass

class SotaSymbol(SotaExpr):
    Table = {}

    def __init__(self, name):
        self.name = name

    def to_string(self):
        return self.name

    to_repr = to_string

def symbol(name):

    sym = SotaSymbol.Table.get(name, None)
    if sym is None:
        sym = SotaSymbol(name)
        SotaSymbol.Table[name] = sym

    return sym

class SotaCons(SotaExpr):
    def __init__(self, car, cdr):
        self.car = car
        self.cdr = cdr

class SotaTuple(SotaExpr):
    pass

class SotaSeq(SotaExpr):
    pass

class SotaList(SotaExpr):
    pass

class SotaDict(SotaExpr):
    pass

class SotaEnum(SotaExpr):
    pass

class SotaFunc(SotaExpr):
    pass

class SotaType(SotaExpr):
    pass

