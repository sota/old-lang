#!/usr/bin/env python

'''
sota: State of the Art

The target below specifies the sota dynamic programming language.
'''
import os
import sys
SCRIPT_PATH, BASENAME = os.path.split(os.path.realpath(__file__) )
SCRIPT_NAME, SCRIPT_EXT = os.path.splitext(os.path.basename(BASENAME) )
sys.path.insert(0, os.path.join(SCRIPT_PATH, 'cli'))
sys.path.insert(0, os.path.join(SCRIPT_PATH, 'pypy'))
os.environ['PYTHONPATH'] = 'src:src/pypy'

from rpython.rtyper.lltypesystem import rffi
from rpython.translator.tool.cbuild import ExternalCompilationInfo

from sast.lexer import Lexer
from sast.parser import Parser

lib_dir = os.path.join(os.getcwd(), 'root/lib')
cli_dir = os.path.join(os.getcwd(), 'src/cli')
cli_eci = ExternalCompilationInfo(
    include_dirs=[cli_dir],
    includes=['cli.h'],
    library_dirs=[lib_dir],
    libraries=['cli'],
    use_cpp_linker=True)
CliToken = rffi.CStruct(
    'CliToken',
    ('name', rffi.CCHARP),
    ('value', rffi.CCHARP))
CliTokenPtr = rffi.CArrayPtr(CliToken)
CliTokensPtr = rffi.CStructPtr(
    'CliTokens',
    ('count', rffi.LONG),
    ('tokens', CliTokenPtr))
c_parse = rffi.llexternal(
    'parse',
    [rffi.LONG, rffi.CCHARPP],
    CliTokensPtr,
    compilation_info=cli_eci)
c_clean = rffi.llexternal(
    'clean',
    [CliTokensPtr],
    rffi.LONG,
    compilation_info=cli_eci)

#######################################################

# __________  Entry point  __________

def entry_point(argv):
    exitcode = 0
    args = {}

    tokens = c_parse(len(argv), rffi.liststr2charpp(argv))
    for i in range(tokens.c_count):
        token = tokens.c_tokens[i]
        name = rffi.charp2str(token.c_name)
        value = rffi.charp2str(token.c_value)
        args[name] = value
    result = c_clean(tokens)
    if result:
        print 'clean unsuccessful'

    lexer = Lexer()
    parser = Parser(lexer)

    if '<source>' in args:
        exitcode = parser.Parse(args['<source>'])
    else:
        exitcode = parser.Repl()

    return exitcode

def target(*args):
    return entry_point

if __name__ == '__main__':
    ep = entry_point(sys.argv)
