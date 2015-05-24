
class SotaToken(object):
    def __init__(self, ts, te, ti, tt, tv, line, pos):
        self.ts = ts        # token start
        self.te = te        # token end
        self.ti = ti        # token id
        self.tt = tt        # token type
        self.tv = tv        # token value
        self.line = line    # token line
        self.pos = pos      # token pos

    def __str__(self):
        return '[%(tt)s %(tv)s]' % vars(self)

    def __repr__(self):
        return self.__str__()
