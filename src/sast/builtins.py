from sast.exceptions import *
from sast.expressions import *


def _add(env, expr, acc):
    if expr.length() < 2:
        raise SastSyntaxError
    args = expr.to_pylist()
    if acc is undefined:
        acc = args[0].eval(env)
        args = args[1:]
    for arg in args:
        acc = acc.add(arg.eval(env))
    return acc

def _sub(env, expr, acc):
    if expr.length() < 2:
        raise SastSyntaxError
    args = expr.to_pylist()
    if acc is undefined:
        acc = args[0].eval(env)
        args = args[1:]
    for arg in args:
        acc = acc.sub(arg.eval(env))
    return acc

def _mul(env, expr, acc):
    if expr.length() < 2:
        raise SastSyntaxError
    args = expr.to_pylist()
    if acc is undefined:
        acc = args[0].eval(env)
        args = args[1:]
    for arg in args:
        acc = acc.mul(arg.eval(env))
    return acc

def _div(env, expr, acc):
    if expr.length() < 2:
        raise SastSyntaxError
    args = expr.to_pylist()
    if acc is undefined:
        acc = args[0].eval(env)
        args = args[1:]
    for arg in args:
        acc = acc.div(arg.eval(env))
    return acc

def assign(env, expr):
    if expr.length() != 2:
        raise SastSyntaxError
    key, value = expr.to_pylist()
    return env.put(key, value.eval(env))

def add(env, expr):
    return _add(env, expr, undefined)

def sub(env, expr):
    return _sub(env, expr, undefined)

def mul(env, expr):
    return _mul(env, expr, undefined)

def div(env, expr):
    return _div(env, expr, undefined)

def add_assign(env, expr):
    if expr.length() < 2:
        raise SastSyntaxError
    symbol = car(expr)
    addends = cdr(expr)
    augend = env.get(symbol)
    result = _add(env, addends, augend)
    return env.put(symbol, result)

def sub_assign(env, expr):
    if expr.length() < 2:
        raise SastSyntaxError
    symbol = car(expr)
    subtrahends = cdr(expr)
    minuend = env.get(symbol)
    result = _sub(env, subtrahends, minuend)
    return env.put(symbol, result)

def mul_assign(env, expr):
    if expr.length() < 2:
        raise SastSyntaxError
    symbol = car(expr)
    multiplicands = cdr(expr)
    multiplier = env.get(symbol)
    result = _mul(env, multiplicands, multiplier)
    return env.put(symbol, result)

def div_assign(env, expr):
    if expr.length() < 2:
        raise SastSyntaxError
    symbol = car(expr)
    divisors = cdr(expr)
    dividend = env.get(symbol)
    result = _mul(env, divisors, dividend)
    return env.put(symbol, result)

def cons(env, expr):
    if not isinstance(expr, SastPair):
        raise SastSyntaxError
    return expr

def list(env, expr):
    args = expr.to_pylist()
    args.reverse()
    cdr = nil
    for car in args:
        cdr = SastPair(car, cdr)
    return cdr
