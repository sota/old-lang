'''
sota: State of the Art

The target below specifies the sota dynamic programming language.
'''
import os

from rpython.rtyper.lltypesystem import rffi, lltype
from rpython.translator.tool.cbuild import ExternalCompilationInfo
src_dir = os.path.join(os.getcwd(), 'src')
cli_dir = os.path.join(src_dir, 'cli')
cli_eci = ExternalCompilationInfo(
    include_dirs=[src_dir, cli_dir],
    includes=['cli.h'],
    library_dirs=[src_dir, cli_dir],
    libraries=['cli'])

parse = rffi.llexternal(
    'parse',
    [lltype.Signed, rffi.CCHARPP],
    lltype.Signed,
    compilation_info=cli_eci)

def debug(msg):
    print 'debug:', msg

# __________  Entry point  __________

def entry_point(argv):
    argv_charpp = rffi.liststr2charpp(argv)
    try:
        parse(len(argv), argv_charpp)
    finally:
        rffi.free_charpp(argv_charpp)

    debug('sota')
    return 0

# _____ Define and setup target ___

def target(*args):
    return entry_point
