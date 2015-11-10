#!/usr/bin/env python

'''
test target for trying out rpython c interfaces
'''
import os
import sys
SCRIPT_PATH, BASENAME = os.path.split(os.path.realpath(__file__) )
SCRIPT_NAME, SCRIPT_EXT = os.path.splitext(os.path.basename(BASENAME) )

from rpython.rtyper.lltypesystem import rffi, lltype
from rpython.translator.tool.cbuild import ExternalCompilationInfo

test_eci = ExternalCompilationInfo(
    include_dirs=['.'],
    includes=['cli.h'],
    library_dirs=['.'],
    libraries=['cli'],
    use_cpp_linker=True)

CLITOKEN = rffi.CStruct(
    'Test',
    ('name', rffi.CCHARP),
    ('value', rffi.CCHARP))
CLITOKENP = rffi.CArrayPtr(CLITOKEN)
CLITOKENPP = rffi.CArrayPtr(CLITOKENP)

c_parse = rffi.llexternal(
    'test',
    [rffi.LONG, rffi.CCHARPP, CLITOKENPP],
    rffi.LONG,
    compilation_info=test_eci)

#######################################################

# __________  Entry point  __________

def entry_point(argv):
    exitcode = 0
    args = {}
    with lltype.scoped_alloc(CLITOKENPP.TO, 1) as c_clitokenpp:
        count = c_parse(len(argv), rffi.liststr2charpp(argv), c_clitokenpp)
        for i in range(count):
            clitoken = c_clitokenpp[0][i]
            name = rffi.charp2str(clitoken.c_name)
            value = rffi.charp2str(clitoken.c_value)
            args[name] = value

    return exitcode

def target(*args):
    return entry_point

if __name__ == '__main__':
    ep = entry_point(sys.argv)
