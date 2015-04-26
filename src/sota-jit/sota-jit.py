'''
sota: State of the Art

The target below specifies the sota dynamic programming language.
'''
import os

from rpython.rtyper.lltypesystem import rffi, lltype
from rpython.translator.tool.cbuild import ExternalCompilationInfo

lexer_dir = os.path.join(os.getcwd(), 'src/lexer')
lexer_eci = ExternalCompilationInfo(
    include_dirs=[lexer_dir],
    includes=['lexer.h'],
    library_dirs=[lexer_dir],
    libraries=['lexer'])

SotaToken = lltype.Struct(
    'SotaToken',
    ('name', rffi.CCHARP),
    ('value', rffi.CCHARP),
    ('line', rffi.LONG),
    ('pos', rffi.LONG))

Point = lltype.GcStruct(
    'Point',
    ('x', lltype.Signed),
    ('y', lltype.Signed))

foo = rffi.llexternal(
    'foo',
    [lltype.Ptr(Point)],
    lltype.Signed,
    compilation_info=lexer_eci)

scan = rffi.llexternal(
    'scan',
    [rffi.CCHARP, lltype.Ptr(SotaToken)],
    rffi.INT,
    compilation_info=lexer_eci)

def loadfile(src):
    return open(src).read()

def debug(msg):
    print 'debug:', msg

# __________  Entry point  __________

def entry_point(argv):

    print 'lexer_dir =', lexer_dir
    tokens = lltype.Ptr(SotaToken)
    pointp = lltype.nullptr(Point)
    r = foo(pointp)
    print lltype.typeOf(r)
    print lltype.typeOf(pointp)
    print lltype.typeOf(pointp.x)
    z = pointp.x + pointp.y
    #print z

    exitcode = 0
    if len(argv) == 2:
        filename, src = argv
        if os.path.isfile(src):
            src = loadfile(src)
        print src
    else:
        print "sota-jit"
        exitcode = 1
    return exitcode

# _____ Define and setup target ___

def target(*args):
    return entry_point