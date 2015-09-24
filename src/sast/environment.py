from sast.exceptions import *
from sast.expressions import *
from sast.expressions import _list

import sast.builtins as builtins

class SastEnv(SastDict):
    pass

Env = SastEnv()

Env.put(
    Cons,
    SastBuiltin(
        Cons,
        SastPair.from_pylist(SastSymbol("car"), SastSymbol("cdr")),
        builtins.cons))

Env.put(
    List,
    SastBuiltin(
        List,
        SastPair.from_pylist(SastSymbol("*items")),
        builtins.list))

Env.put(
    Assign,
    SastBuiltin(
        Assign,
        SastPair.from_pylist(SastSymbol("symbol"), SastSymbol("value")),
        builtins.assign))

Env.put(
    Add,
    SastBuiltin(
        Add,
        SastPair.from_pylist(SastSymbol("augend"), SastSymbol("*addends")),
        builtins.add))

Env.put(
    Sub,
    SastBuiltin(
        Sub,
        SastPair.from_pylist(SastSymbol("minuend"), SastSymbol("*subtrahends")),
        builtins.sub))

Env.put(
    Mul,
    SastBuiltin(
        Mul,
        SastPair.from_pylist(SastSymbol("multiplier"), SastSymbol("*multiplicands")),
        builtins.mul))

Env.put(
    Div,
    SastBuiltin(
        Div,
        SastPair.from_pylist(SastSymbol("dividend"), SastSymbol("*divisors")),
        builtins.div))

Env.put(
    AddAssign,
    SastBuiltin(
        AddAssign,
        SastPair.from_pylist(SastSymbol("symbol"), SastSymbol("*addends")),
        builtins.add_assign))

Env.put(
    SubAssign,
    SastBuiltin(
        SubAssign,
        SastPair.from_pylist(SastSymbol("symbol"), SastSymbol("*subtrahends")),
        builtins.sub_assign))

Env.put(
    MulAssign,
    SastBuiltin(
        MulAssign,
        SastPair.from_pylist(SastSymbol("symbol"), SastSymbol("*multiplicands")),
        builtins.mul_assign))

Env.put(
    DivAssign,
    SastBuiltin(
        DivAssign,
        SastPair.from_pylist(SastSymbol("symbol"), SastSymbol("*divisors")),
        builtins.div_assign))

