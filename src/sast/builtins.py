from sast.exceptions import *
from sast.expressions import *

from sast.expressions import _list


def op(env, expr, acc, func):
    if expr.length():
        args = expr.to_pylist()
        if acc is undefined:
            acc = args[0].eval(env)
            args = args[1:]
        for arg in args:
            acc = func(acc, arg.eval(env))
        return acc
    raise SastSyntaxError

def assign(env, expr):
    if expr.length() != 2:
        raise SastSyntaxError
    if not car(expr).is_symbol():
        raise SastSyntaxError
    key, value = expr.to_pylist()
    return env.put(key, value.eval(env))

def add(env, expr):
    return op(env, expr, undefined, lambda acc, arg: acc.add(arg))

def sub(env, expr):
    return op(env, expr, undefined, lambda acc, arg: acc.sub(arg))

def mul(env, expr):
    return op(env, expr, undefined, lambda acc, arg: acc.mul(arg))

def div(env, expr):
    return op(env, expr, undefined, lambda acc, arg: acc.div(arg))

def add_assign(env, expr):
    symbol = car(expr)
    result = op(env, cdr(expr), env.get(symbol), lambda acc, arg: acc.add(arg))
    return assign(env, _list(symbol, result))

def sub_assign(env, expr):
    symbol = car(expr)
    result = op(env, cdr(expr), env.get(symbol), lambda acc, arg: acc.sub(arg))
    return assign(env, _list(symbol, result))

def mul_assign(env, expr):
    symbol = car(expr)
    result = op(env, cdr(expr), env.get(symbol), lambda acc, arg: acc.mul(arg))
    return assign(env, _list(symbol, result))

def div_assign(env, expr):
    symbol = car(expr)
    result = op(env, cdr(expr), env.get(symbol), lambda acc, arg: acc.mul(arg))
    return assign(env, _list(symbol, result))

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
