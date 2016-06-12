from sast.exceptions import *
from sast.expressions import (
    SastPair,
    SastSymbol,
    SastBuiltin,
    undefined,
    car,
    cdr,
    nil)

from sast.expressions import _list

def New(name, **kwargs):
    env = kwargs.pop("env")
    obj = type(name, (SastBuiltin,), kwargs)(env)
    obj.idx = 1 if "Assign" in name else 0
    return obj

def Cons(self, exp, env):
    if not isinstance(exp, SastPair):
        raise SastSyntaxError
    return exp

def List(self, exp, env):
    args = exp.to_pylist()
    args.reverse()
    cdr = nil
    for car in args:
        cdr = SastPair(car, cdr)
    return cdr

def Print(self, exp, env):
    print " ".join([arg.to_str() for arg in exp.to_pylist()])
    return exp

class SastApply(SastBuiltin):
    pass

class SastEval(SastBuiltin):
    pass

def op(exp, env, acc, func):
    if exp.length():
        args = exp.to_pylist()
        if acc is undefined:
            acc = args[0] #FIXME: this should be a default, or something
            args = args[1:]
        for arg in args:
            acc = func(acc, arg)
        return acc
    raise SastSyntaxError

def Add(self, exp, env):
    return op(exp, env, undefined, lambda acc, arg: acc.add(arg))

def Sub(self, exp, env):
    return op(exp, env, undefined, lambda acc, arg: acc.sub(arg))

def Mul(self, exp, env):
    return op(exp, env, undefined, lambda acc, arg: acc.mul(arg))

def Div(self, exp, env):
    return op(exp, env, undefined, lambda acc, arg: acc.div(arg))

def Assign(self, exp, env):
    if exp.length() != 2:
        raise SastSyntaxError
    if not car(exp).is_symbol():
        raise SastSyntaxError
    key, value = exp.to_pylist()
    return env.Set(key, value.Eval(env))

def AddAssign(self, exp, env):
    symbol = car(exp)
    result = op(cdr(exp), env, env.Get(symbol), lambda acc, arg: acc.add(arg))
    return Assign(self, _list(symbol, result), env)

def SubAssign(self, exp, env):
    symbol = car(exp)
    result = op(cdr(exp), env, env.Get(symbol), lambda acc, arg: acc.sub(arg))
    return Assign(self, _list(symbol, result), env)

def MulAssign(self, exp, env):
    symbol = car(exp)
    result = op(cdr(exp), env, env.Get(symbol), lambda acc, arg: acc.mul(arg))
    return Assign(self, _list(symbol, result), env)

def DivAssign(self, exp, env):
    symbol = car(exp)
    result = op(cdr(exp), env, env.Get(symbol), lambda acc, arg: acc.mul(arg))
    return Assign(self, _list(symbol, result), env)

