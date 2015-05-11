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

def parse(source):
    tokens = lexer.scan(source)
    for token in tokens:
        print '%s %s' % (token.type, token.value)
    return 0

def repl(prompt='sota>'):
    pass
