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

foo = rffi.llexternal(
    'foo',
    [],
    lltype.Void,
    compilation_info=cli_eci)

bar = rffi.llexternal(
    'bar',
    [lltype.Signed],
    lltype.Signed,
    compilation_info=cli_eci)

baz = rffi.llexternal(
    'baz',
    [lltype.Signed, rffi.CCHARP],
    lltype.Signed,
    compilation_info=cli_eci)

parse = rffi.llexternal(
    'parse',
    [lltype.Signed,lltype.Ptr(lltype.Array(rffi.CCHARP, hints={'nolength': True}))],
    lltype.Signed,
    compilation_info=cli_eci)

def debug(msg):
    print 'debug:', msg

# __________  Entry point  __________

def entry_point(argv):
    print 'argv =', argv

    args = ' '.join(argv[1:])
    args = ''
    for arg in argv:
        args += ' '
        if ' ' in arg:
            args += '"' + arg + '"'
        else:
            args += arg
    print 'args =', args
    if isinstance(argv, list):
        print 'isinstance of list'
    if len(argv) and isinstance(argv[0], str):
        print 'argv[0] isinstance of str'

    foo()
    print 'bar_result =', bar(13)
    print 'baz_result =', baz(-13, "donkeypunch")
    parse(2, ["donkey", "punch"])

    debug('sota')
    return 0

# _____ Define and setup target ___

def target(*args):
    return entry_point
