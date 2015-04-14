'''
sota: State of the Art

The target below specifies the sota dynamic programming language.
'''
import os

from rpython.rtyper.lltypesystem import rffi, lltype
from rpython.translator.tool.cbuild import ExternalCompilationInfo

cli_dir = os.path.join(os.getcwd(), 'src/cli')
cli_eci = ExternalCompilationInfo(
    include_dirs=[cli_dir],
    includes=['cli.h'],
    library_dirs=[cli_dir],
    libraries=['cli'])

parse = rffi.llexternal(
    'parse',
    [lltype.Signed, rffi.CCHARPP],
    lltype.Signed,
    compilation_info=cli_eci)

lexer_dir = os.path.join(os.getcwd(), 'src/lexer')
lexer_eci = ExternalCompilationInfo(
    include_dirs=[lexer_dir],
    includes =['lexer.h'],
    library_dirs=[lexer_dir],
    libraries=['lexer'])

scan = rffi.llexternal(
    'scan',
    [rffi.CCHARP],
    lltype.Signed,
    compilation_info=lexer_eci)

def debug(msg):
    print 'debug:', msg

# __________  Entry point  __________

def entry_point(argv):
    argv_charpp = rffi.liststr2charpp(argv)
    try:
        exitcode = parse(len(argv), argv_charpp)
        #result = scan("sota baby")
    finally:
        rffi.free_charpp(argv_charpp)

    return exitcode

# _____ Define and setup target ___

def target(*args):
    return entry_point
