#!/usr/bin/env python

'''
test target for trying out rpython c interfaces
'''
import os
import sys
SCRIPT_PATH, BASENAME = os.path.split(os.path.realpath(__file__) )
SCRIPT_NAME, SCRIPT_EXT = os.path.splitext(os.path.basename(BASENAME) )

sys.path.insert(0, os.path.join(SCRIPT_PATH, 'src/pypy'))
from rpython.rtyper.lltypesystem import rffi, lltype
from rpython.translator.tool.cbuild import ExternalCompilationInfo

root_dir = os.getcwd()
test_eci = ExternalCompilationInfo(
    include_dirs=[root_dir],
    includes=['test.h'],
    library_dirs=[root_dir],
    libraries=['test'],
    use_cpp_linker=True)

PAIR = rffi.CStruct(
    'Pair',
    ('name', rffi.CCHARP),
    ('value', rffi.CCHARP))
PAIRP = rffi.CArrayPtr(PAIR)
PAIRPP = rffi.CArrayPtr(PAIRP)

c_test1 = rffi.llexternal(
    'test1',
    [PAIRPP],
    rffi.LONG,
    compilation_info=test_eci)

c_test2 = rffi.llexternal(
    'test2',
    [PAIRP],
    rffi.LONG,
    compilation_info=test_eci)

#######################################################

# __________  Entry point  __________

def entry_point(argv):
    exitcode = 0
    args = {}
    with lltype.scoped_alloc(PAIRPP.TO, 1) as c_pairpp:
        count = c_test1(c_pairpp)
        print 'count =', count
        for i in range(count):
            pair = c_pairpp[0][i]
            name = rffi.charp2str(pair.c_name)
            value = rffi.charp2str(pair.c_value)
            print 'Pair {name=%s, value=%s}' % (name, value)
            args[name] = value

    return exitcode

def target(*args):
    return entry_point

if __name__ == '__main__':
    sys.exit(entry_point(sys.argv))
