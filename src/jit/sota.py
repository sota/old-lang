'''
sota: State of the Art

The target below specifies the sota dynamic programming language.
'''
import os

from rpython.translator.unsimplify import varoftype
from rpython.rtyper.lltypesystem import rffi, lltype
from rpython.rtyper.tool import rffi_platform as platform
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

#PointGc = lltype.GcStruct(
#    'Point',
#    ('x', lltype.Signed),
#    ('y', lltype.Signed))

CPOINT = rffi.CStruct(
    'Point',
    ('x', rffi.LONG),
    ('y', rffi.LONG))
CPOINTP = rffi.CArrayPtr(CPOINT)
CPOINTPP = rffi.CArrayPtr(CPOINTP)
#CCHARP = lltype.Ptr(lltype.Array(lltype.Char, hints={'nolength': True}))
#CCHARPP = lltype.Ptr(lltype.Array(CCHARP, hints={'nolength': True}))
#PointPtr = rffi.CStructPtr(
#    'Point',
#    ('x', rffi.LONG),
#    ('y', rffi.LONG))
#PointArray = rffi.CArrayPtr(Point)

foo = rffi.llexternal(
    'foo',
    [CPOINTPP],
    rffi.LONG,
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
    if len(argv) != 2:
        print 'sota-jit only takes one argument <text|file>'
        return 1
    source = argv[1]
    if os.path.isfile(source):
        print 'source is file'
    else:
        print 'source is text'

#    with lltype.scoped_alloc(CPOINTPP.TO, 1) as cpointpp:
#        count = foo(cpointpp)
#        cpointp = cpointpp[0]
#        for i in range(count):
#            cpoint = cpointp[i]
#            print 'Point {x=%d, %d}' % (cpoint.c_x, cpoint.c_y)
    print 'sota success'
    return 0

def target(*args):
    return entry_point
