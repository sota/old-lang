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

def Cons(self, env, exp):
    if not isinstance(exp, SastPair):
        raise SastSyntaxError
    return exp

def List(self, env, exp):
    args = exp.to_pylist()
    args.reverse()
    cdr = nil
    for car in args:
        cdr = SastPair(car, cdr)
    return cdr

def Print(self, env, exp):
    print " ".join([arg.to_str() for arg in exp.to_pylist()])
    return exp

class SastApply(SastBuiltin):
    pass

class SastEval(SastBuiltin):
    pass

def op(env, exp, acc, func):
    if exp.length():
        args = exp.to_pylist()
        if acc is undefined:
            acc = args[0].Eval(env)
            args = args[1:]
        for arg in args:
            acc = func(acc, arg.Eval(env))
        return acc
    raise SastSyntaxError

def Add(self, env, exp):
    return op(env, exp, undefined, lambda acc, arg: acc.add(arg))

def Sub(self, env, exp):
    return op(env, exp, undefined, lambda acc, arg: acc.sub(arg))

def Mul(self, env, exp):
    return op(env, exp, undefined, lambda acc, arg: acc.mul(arg))

def Div(self, env, exp):
    return op(env, exp, undefined, lambda acc, arg: acc.div(arg))

def Assign(self, env, exp):
    if exp.length() != 2:
        raise SastSyntaxError
    if not car(exp).is_symbol():
        raise SastSyntaxError
    key, value = exp.to_pylist()
    return env.Set(key, value.Eval(env))

def AddAssign(self, env, exp):
    symbol = car(exp)
    result = op(env, cdr(exp), env.Get(symbol), lambda acc, arg: acc.add(arg))
    return Assign(self, env, _list(symbol, result))

def SubAssign(self, env, exp):
    symbol = car(exp)
    result = op(env, cdr(exp), env.Get(symbol), lambda acc, arg: acc.sub(arg))
    return Assign(self, env, _list(symbol, result))

def MulAssign(self, env, exp):
    symbol = car(exp)
    result = op(env, cdr(exp), env.Get(symbol), lambda acc, arg: acc.mul(arg))
    return Assign(self, env, _list(symbol, result))

def DivAssign(self, env, exp):
    symbol = car(exp)
    result = op(env, cdr(exp), env.Get(symbol), lambda acc, arg: acc.mul(arg))
    return Assign(self, env, _list(symbol, result))

