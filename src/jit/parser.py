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
        print '[%s]' % token.tv
    else:
        print '[%s %s]' % (token.tt, token.tv)

def parse(source):
    tokens = lexer.scan(source)
    for token in tokens:
        printtoken(token)
    return 0

def repl(prompt='sota>'):
    pass
