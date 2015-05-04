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

CLITOKEN = rffi.CStruct(
    'CliToken',
    ('name', rffi.CCHARP),
    ('value', rffi.CCHARP))
CLITOKENP = rffi.CArrayPtr(CLITOKEN)
CLITOKENPP = rffi.CArrayPtr(CLITOKENP)

parse = rffi.llexternal(
    'parse',
    [rffi.LONG, rffi.CCHARPP, CLITOKENPP],
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

SOTATOKEN = rffi.CStruct(
    'SotaToken',
    ('ts', rffi.LONG),
    ('te', rffi.LONG),
    ('type', rffi.LONG))
SOTATOKENP = rffi.CArrayPtr(SOTATOKEN)
SOTATOKENPP = rffi.CArrayPtr(SOTATOKENP)

scan = rffi.llexternal(
    'scan',
    [rffi.CONST_CCHARP, SOTATOKENPP],
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

    with lltype.scoped_alloc(CLITOKENPP.TO, 1) as cclitokenpp:
        result = parse(len(argv), rffi.liststr2charpp(argv), cclitokenpp)
        for i in range(result):
            clitoken = cclitokenpp[0][i]
            print 'CliToken {name=%s, value=%s}' % (rffi.charp2str(clitoken.c_name), rffi.charp2str(clitoken.c_value))
        print 'result =', result

    source = argv[1]
    source = loadfile(source) if os.path.isfile(source) else source + '\n'

    with lltype.scoped_alloc(SOTATOKENPP.TO, 1) as csotatokenpp:
        sotacode = rffi.cast(rffi.CONST_CCHARP, rffi.str2charp(source))
        result = scan(sotacode, csotatokenpp)
        for i in range(result):
            token = deref(csotatokenpp)[i]
            ts = rffi.cast(rffi.SIZE_T, token.c_ts)
            te = rffi.cast(rffi.SIZE_T, token.c_te)
            print '{ts=%s, te=%s, type=%s value=%s}' % (ts, te, token.c_type, source[ts:te])
    return 0

def target(*args):
    return entry_point
