
class SastExpr(object):

    def __init__(self):
        self.value = None

    def to_string(self):
        return str(self.value)

class SastUndefined(SastExpr):

    def __init__(self):
        self.value = '<undefined>'

class SastAtom(SastExpr):

    def __init__(self, value):
        self.value = value

class SastFixnum(SastAtom):

    def __init__(self, value):
        self.value = value

class SastString(SastAtom):

    def __init__(self, value):
        self.value = value

    def to_string(self):
        return '"' + self.value + '"'

class SastSymbol(SastAtom):

    _table = {}

    def __new__(cls, value):
        symbol = cls._table.get(value, None)
        if not symbol:
            cls._table[value] = symbol = super(SastSymbol, cls).__new__(cls, value)
        return symbol

    def __init__(self, value):
        self.value = value

class SastList(SastExpr):
    pass

class SastNil(SastList):

    _nil = None

    def __new__(cls):
        if not cls._nil:
            cls._nil = super(SastNil, cls).__new__(cls)
        return cls._nil

    def __values__(self):
        return []

    def to_string(self):
        return '()'

nil = SastNil()

class SastPair(SastList):

    def __init__(self, car, cdr=nil):
        self.car = car
        self.cdr = cdr

    def __values__(self):
        values = [self.car]
        values.extend(self.cdr.__values__())
        return values

    def to_string(self):
        return '(' + ' '.join([value.to_string() for value in self.__values__()]) + ')'
