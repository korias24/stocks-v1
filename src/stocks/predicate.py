# -*- coding: utf-8 -*-

import functools

def notp(p):
    def _p(x):
        return not p(x)

    return _p

def binop(op, *ps):
    def _p(x):
        return functools.reduce(op, [p(x) for p in ps])

    return _p

def andp(*ps):
    return binop(lambda x, y: x and y, *ps)

def orp(*ps):
    return binop(lambda x, y: x or y, *ps)

def lt(v):
    def p(x):
        return x < v

    return p

def gt(v):
    def p(x):
        return x > v

    return p

def lte(v):
    return notp(gt(v))

def gte(v):
    return notp(lt(v))

def eql(v):
    def p(x):
        return x == v

    return p

def neql(v):
    return notp(eql(v))
