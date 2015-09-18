
from sast.expressions import *

class SastEnv(SastDict):
    pass

Env = SastEnv()

def assign(env, expr):
    key, value = expr.to_pylist()
    return env.assign(key, value.eval(env))

Env.assign(
    assign_symbol,
    SastBuiltin(
        assign_symbol,
        SastPair.from_pylist(SastSymbol("symbol"), SastSymbol("value")),
        assign))

def add(env, expr, acc=None):
    args = expr.to_pylist()
    if not acc:
        acc = args[0].eval(env)
        args = args[1:]
    for arg in args:
        acc = acc.add(arg.eval(env))
    return acc

Env.assign(
    add_symbol,
    SastBuiltin(
        add_symbol,
        SastPair.from_pylist(SastSymbol("augend"), SastSymbol("*addends")),
        add))

def sub(env, expr, acc=None):
    args = expr.to_pylist()
    if not acc:
        acc = args[0].eval(env)
        args = args[1:]
    for arg in args:
        acc = acc.sub(arg.eval(env))
    return acc

Env.assign(
    sub_symbol,
    SastBuiltin(
        sub_symbol,
        SastPair.from_pylist(SastSymbol("minuend"), SastSymbol("*subtrahends")),
        sub))

def mul(env, expr, acc=None):
    args = expr.to_pylist()
    if not acc:
        acc = args[0].eval(env)
        args = args[1:]
    for arg in args:
        acc = acc.mul(arg.eval(env))
    return acc

Env.assign(
    mul_symbol,
    SastBuiltin(
        mul_symbol,
        SastPair.from_pylist(SastSymbol("multiplier"), SastSymbol("*multiplicands")),
        mul))

def div(env, expr, acc=None):
    args = expr.to_pylist()
    if not acc:
        acc = args[0].eval(env)
        args = args[1:]
    for arg in args:
        acc = acc.div(arg.eval(env))
    return acc

Env.assign(
    div_symbol,
    SastBuiltin(
        div_symbol,
        SastPair.from_pylist(SastSymbol("dividend"), SastSymbol("*divisors")),
        div))

