from sast.exceptions import *
from sast.expressions import *
from sast.expressions import _list
import sast.builtins as builtins

class SastEnv(SastDict):
    pass
#    def __init__(self, keys=(), values=(), parent=None):
#        self.parent = parent
#        if len(keys) != len(values):
#            raise TypeError("expected: %s, given: %s" % (keys, values))
#        for i in xrange(len(keys)):
#            self.insert(keys[i], values[i])
#    def Get(self, symbol):
#        value = super(SastEnv, self).Get(symbol)
#        if value == undefined and parent:
#            value = parent.Get(symbol)
#        if value == undefined:
#            raise TypeError("something effed up!")
#        return value

Env = SastEnv()
Env.Set(Cons,       builtins.New("SastCons", env=Env, call=builtins.Cons))
Env.Set(List,       builtins.New("SastList", env=Env, call=builtins.List))
Env.Set(Print,      builtins.New("SastPrint", env=Env, call=builtins.Print))
Env.Set(Add,        builtins.New("SastAdd", env=Env, call=builtins.Add))
Env.Set(Sub,        builtins.New("SastSub", env=Env, call=builtins.Sub))
Env.Set(Mul,        builtins.New("SastMul", env=Env, call=builtins.Mul))
Env.Set(Div,        builtins.New("SastDiv", env=Env, call=builtins.Div))
Env.Set(Assign,     builtins.New("SastAssign", env=Env, call=builtins.Assign))
Env.Set(AddAssign,  builtins.New("SastAddAssign", env=Env, call=builtins.AddAssign))
Env.Set(SubAssign,  builtins.New("SastSubAssign", env=Env, call=builtins.SubAssign))
Env.Set(MulAssign,  builtins.New("SastMulAssign", env=Env, call=builtins.MulAssign))
Env.Set(DivAssign,  builtins.New("SastDivAssign", env=Env, call=builtins.DivAssign))
