'''
sota: State of the Art

The target below specifies the sota dynamic programming language.
'''

def debug(msg):
    print 'debug:', msg

# __________  Entry point  __________

def entry_point(argv):
    debug('sota')
    return 0

# _____ Define and setup target ___

def target(*args):
    return entry_point
