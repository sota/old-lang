#!/usr/bin/env python

import sys
sys.dont_write_bytecode = True
import inspect
from subprocess import check_output, check_call

sotasrc = 'targetsota.py'
python = 'python' if check_call('which pypy', shell=True) else 'pypy'
python = 'python' # FIXME:  its slower; doing this for now ... -sai
rpython = 'repos/pypy/rpython/bin/rpython'

def env():
    try:
        frame = inspect.currentframe().f_back
        return dict(frame.f_globals.items() + frame.f_locals.items() )
    finally:
        del frame

def task_pyflakes():
    return {
        'actions': ['pyflakes %(sotasrc)s' % env() ],
    }

def task_submod_update():
    output = check_output('git submodule', shell=True)
    submods = [ line.split()[1] for line in output.strip().split('\n') ]
    for submod in submods:
        yield {
            'name': submod,
            'actions': ['git submodule update --init %(submod)s' % env() ],
            'targets': [submod]
        }

def task_build_sota():
    return {
        'actions': ['%(python)s %(rpython)s %(sotasrc)s' % env() ],
        'file_dep': [rpython],
        'teardown': ['mv targetsota-c sota'],
        'targets': ['sota'],
    }

#def task_rename():
#    return {
#        'actions': ['cp build/targetsota-c sota'],
#        'file_dep': ['build/targetsota-c'],
#        'targets': ['sota'],
#    }
