
from rpython.rtyper.lltypesystem import rffi, lltype

class Token(object): #pylint: disable=too-few-public-methods

    def __init__(self, name, value, kind, line, pos, skip):
        self.name = name
        self.value = value
        self.kind = kind
        self.line = line
        self.pos = pos
        self.skip = skip

    def to_str(self):
        return '[name=%s value=%s kind=%d line=%d pos=%d skip=%s]' % (
            self.name,
            self.value,
            self.kind,
            self.line,
            self.pos,
            self.skip)

    def is_name(self, *names):
        for name in list(names):
            if name == self.name:
                return True
        return False
