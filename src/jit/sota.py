'''
sota: State of the Art

The target below specifies the sota dynamic programming language.
'''
import os

from rpython.translator.unsimplify import varoftype
from rpython.rtyper.lltypesystem import rffi, lltype
from rpython.rtyper.tool import rffi_platform as platform
from rpython.translator.tool.cbuild import ExternalCompilationInfo

cli_dir = os.path.join(os.getcwd(), 'src/cli')
cli_eci = ExternalCompilationInfo(
    include_dirs=[cli_dir],
    includes=['cli.h'],
    library_dirs=[cli_dir],
    libraries=['cli'],
    use_cpp_linker=True)

CCLITOKEN = rffi.CStruct(
    'CliToken',
    ('name', rffi.CCHARP),
    ('value', rffi.CCHARP))
CCLITOKENP = rffi.CArrayPtr(CCLITOKEN)
CCLITOKENPP = rffi.CArrayPtr(CCLITOKENP)

parse = rffi.llexternal(
    'parse',
    [rffi.LONG, rffi.CCHARPP, CCLITOKENPP],
    rffi.LONG,
    compilation_info=cli_eci)

#######################################################

lexer_dir = os.path.join(os.getcwd(), 'src/lexer')
lexer_eci = ExternalCompilationInfo(
    include_dirs=[lexer_dir],
    includes=['lexer.h'],
    library_dirs=[lexer_dir],
    libraries=['lexer'],
    use_cpp_linker=True)

CSOTATOKEN = rffi.CStruct(
    'SotaToken',
    ('index', rffi.SIZE_T),
    ('length', rffi.SIZE_T),
    ('type', rffi.SIZE_T))
CSOTATOKENP = rffi.CArrayPtr(CSOTATOKEN)
CSOTATOKENPP = rffi.CArrayPtr(CSOTATOKENP)

scan = rffi.llexternal(
    'scan',
    [rffi.CONST_CCHARP, CSOTATOKENPP],
    rffi.LONG,
    compilation_info=lexer_eci)

def loadfile(source):
    return open(source).read()

def debug(msg):
    print 'debug:', msg

def deref(obj):
    return obj[0]

# __________  Entry point  __________

def entry_point(argv):

    with lltype.scoped_alloc(CCLITOKENPP.TO, 1) as cclitokenpp:
        result = parse(len(argv), rffi.liststr2charpp(argv), cclitokenpp)
        for i in range(result):
            clitoken = cclitokenpp[0][i]
            print 'CliToken {name=%s, value=%s}' % (rffi.charp2str(clitoken.c_name), rffi.charp2str(clitoken.c_value))
        print 'result =', result

    source = argv[1]
    source = loadfile(source) if os.path.isfile(source) else source + '\n'

    with lltype.scoped_alloc(CSOTATOKENPP.TO, 1) as csotatokenpp:
        sotacode = rffi.cast(rffi.CONST_CCHARP, rffi.str2charp(source))
        result = scan(sotacode, csotatokenpp)
        for i in range(result):
            token = deref(csotatokenpp)[i]
            print token.c_type
    return 0

def target(*args):
    return entry_point
