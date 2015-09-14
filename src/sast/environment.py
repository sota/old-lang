
from sast.expressions import *

class SastEnv(SastDict):
    pass

Env = SastEnv()

def assign(env, expr):
    key, value = expr.to_pylist()
    return env.assign(key, value.eval(env))

Env.assign(
    SastSymbol("="),
    SastBuiltin(
        SastPair.from_pylist(SastSymbol("key"), SastSymbol("value")),
        assign))

def add(env, expr):
    x, y = expr.to_pylist()
    return x.eval(env).add(y.eval(env))

Env.assign(
    SastSymbol("+"),
    SastBuiltin(
        SastPair.from_pylist(SastSymbol("x"), SastSymbol("y")),
        add))

def sub(env, expr):
    x, y = expr.to_pylist()
    return x.eval(env).sub(y.eval(env))

Env.assign(
    SastSymbol("-"),
    SastBuiltin(
        SastPair.from_pylist(SastSymbol("x"), SastSymbol("y")),
        sub))

def mul(env, expr):
    x, y = expr.to_pylist()
    return x.eval(env).mul(y.eval(env))

Env.assign(
    SastSymbol("*"),
    SastBuiltin(
        SastPair.from_pylist(SastSymbol("x"), SastSymbol("y")),
        mul))

def div(env, expr):
    x, y = expr.to_pylist()
    return x.eval(env).div(y.eval(env))

Env.assign(
    SastSymbol("/"),
    SastBuiltin(
        SastPair.from_pylist(SastSymbol("x"), SastSymbol("y")),
        div))

