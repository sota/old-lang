'''
sota: State of the Art

The target below specifies the sota dynamic programming language.
'''
import os
lexer_dir = os.path.join(os.getcwd(), 'src/lexer')
lexer_h = 'lexer.h'
liblexer_a = 'lexer'

from rpython.rtyper.lltypesystem import rffi, lltype
from rpython.translator.tool.cbuild import ExternalCompilationInfo
eci = ExternalCompilationInfo(include_dirs=[lexer_dir], includes=[lexer_h], library_dirs=[lexer_dir], libraries=[liblexer_a])
foo = rffi.llexternal('foo', [], lltype.Void, compilation_info=eci)

def debug(msg):
    print 'debug:', msg

# __________  Entry point  __________

def entry_point(argv):
    foo()
    debug('sota')
    return 0

# _____ Define and setup target ___

def target(*args):
    return entry_point
