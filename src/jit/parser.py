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
    if token.name == token.value:
        print '[%s,%s %s]' % (token.line, token.pos, token.value)
    else:
        print '[%s,%s %s:%s]' % (token.line, token.pos, token.name, token.value)

def parse(source):
    tokens = lexer.scan(source)
    for token in tokens:
        printtoken(token)
    return 0

def repl(prompt='sota>'):
    pass
