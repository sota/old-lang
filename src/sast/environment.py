from sast.exceptions import *
from sast.expressions import *
from sast.expressions import _list
import sast.builtins as builtins

class SastEnv(SastDict):
    pass

Env = SastEnv()
Env.Set(Cons,       builtins.New("SastCons", env=Env, call=builtins.Cons))
Env.Set(List,       builtins.New("SastList", env=Env, call=builtins.List))
Env.Set(Print,      builtins.New("SastPrint", env=Env, call=builtins.Print))
Env.Set(Add,        builtins.New("SastAdd", env=Env, call=builtins.Add))
Env.Set(Sub,        builtins.New("SastSub", env=Env, call=builtins.Sub))
Env.Set(Mul,        builtins.New("SastMul", env=Env, call=builtins.Mul))
Env.Set(Div,        builtins.New("SastDiv", env=Env, call=builtins.Div))
