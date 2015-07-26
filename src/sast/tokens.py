
class SotaToken(object): #pylint: disable=too-few-public-methods
    def __init__(self, name, value, line, pos):
        self.name = name
        self.value = value
        self.line = line
        self.pos = pos

    def __str__(self):
        return '[%(name)s %(value)s]' % vars(self)

    def __repr__(self):
        return self.__str__()
