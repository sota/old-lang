'''
sota: State of the Art

The target below specifies the sota dynamic programming language.
'''
import os

from rpython.rtyper.lltypesystem import rffi, lltype
from rpython.translator.tool.cbuild import ExternalCompilationInfo

import parser

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

c_parse = rffi.llexternal(
    'parse',
    [rffi.LONG, rffi.CCHARPP, CLITOKENPP],
    rffi.LONG,
    compilation_info=cli_eci)

def loadfile(source):
    return open(source).read()

#######################################################

# __________  Entry point  __________

def entry_point(argv):

    with lltype.scoped_alloc(CLITOKENPP.TO, 1) as cclitokenpp:
        result = c_parse(len(argv), rffi.liststr2charpp(argv), cclitokenpp)
        print 'result =', result
        for i in range(result):
            clitoken = cclitokenpp[0][i]
            print 'CliToken {name=%s, value=%s}' % (rffi.charp2str(clitoken.c_name), rffi.charp2str(clitoken.c_value))

    source = argv[1]
    source = loadfile(source) if os.path.isfile(source) else source + '\n'
    exitcode = parser.parse(source)
    return exitcode

def target(*args):
    return entry_point
