import os

import lexer

def debug(msg):
    print 'debug:', msg

def read():
    pass

def expand():
    pass

def evaluate():
    pass

def printtoken(token):
    if token.tt == token.tv:
        print '[%d,%d %d:%d %s:%d]' % (token.line, token.pos, token.ts, token.te, token.tv, token.ti)
    else:
        print '[%d,%d %d:%d %s|%s:%d]' % (token.line, token.pos, token.ts, token.te, token.tt, token.tv, token.ti)

def parse(source):
    tokens = lexer.scan(source)
    for token in tokens:
        printtoken(token)
    return 0

def repl(prompt='sota>'):
    pass
