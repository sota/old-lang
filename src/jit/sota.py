'''
sota: State of the Art

The target below specifies the sota dynamic programming language.
'''
import os

from rpython.rtyper.lltypesystem import rffi, lltype
from rpython.translator.tool.cbuild import ExternalCompilationInfo

import parser
from version import SOTA_VERSION

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

def load_source(source):
    if os.path.isfile(source):
        return open(source).read()
    return source + '\n'

def exec_source(source):
    return parser.parse(source)

def sota_exec(args):
    source = args['<source>']
    source = load_source(source)
    return exec_source(source)

def stdin_readline():
    line = ''
    c = os.read(0, 1)
    while '\n' != c:
        line += c
        c = os.read(0, 1)
    return line

def sota_repl(args):
    exitcode = 0
    prompt = 'sota> '

    print 'sota %s repl:' % SOTA_VERSION
    print 'ctrl+c | ctrl+d, return to exit'
    print
    while True:
        os.write(1, prompt)
        source = None
        try:
            source = stdin_readline()
        except KeyboardInterrupt:
            break
        except EOFError:
            break
        if not source:
            break

        print source

    return exitcode

#######################################################

# __________  Entry point  __________

def entry_point(argv):
    exitcode = 0
    args = {}
    with lltype.scoped_alloc(CLITOKENPP.TO, 1) as cclitokenpp:
        result = c_parse(len(argv), rffi.liststr2charpp(argv), cclitokenpp)
        for i in range(result):
            clitoken = cclitokenpp[0][i]
            args[rffi.charp2str(clitoken.c_name)] = rffi.charp2str(clitoken.c_value)

    if '<source>' in args:
        exitcode = sota_exec(args)
    else:
        exitcode = sota_repl(args)

    return exitcode

def target(*args):
    return entry_point
