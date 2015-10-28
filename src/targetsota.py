#!/usr/bin/env python

'''
sota: State of the Art

The target below specifies the sota dynamic programming language.
'''
import os
import sys
sys.path.insert(0, 'src')
sys.path.insert(0, 'src/cli')
sys.path.insert(0, 'lib/pypy')
os.environ['PYTHONPATH'] = 'src:src/pypy'

from rpython.rtyper.lltypesystem import rffi, lltype
from rpython.translator.tool.cbuild import ExternalCompilationInfo

from sast.lexer import Lexer
from sast.parser import Parser

lib_dir = os.path.join(os.getcwd(), 'lib')
cli_dir = os.path.join(os.getcwd(), 'src/cli')
cli_eci = ExternalCompilationInfo(
    include_dirs=[cli_dir],
    includes=['cli.h'],
    library_dirs=[lib_dir],
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
    return source

#######################################################

# __________  Entry point  __________

def entry_point(argv):
    exitcode = 0
    args = {}
    with lltype.scoped_alloc(CLITOKENPP.TO, 1) as c_clitokenpp:
        result = c_parse(len(argv), rffi.liststr2charpp(argv), c_clitokenpp)
        for i in range(result):
            clitoken = c_clitokenpp[0][i]
            args[rffi.charp2str(clitoken.c_name)] = rffi.charp2str(clitoken.c_value)

    lexer = Lexer()
    parser = Parser(lexer)

    if '<source>' in args:
        exitcode = parser.Parse(load_source(args['<source>']))
    else:
        exitcode = parser.Repl()

    return exitcode

def target(*args):
    return entry_point

if __name__ == '__main__':
    ep = entry_point(sys.argv)
    print 'hi'
