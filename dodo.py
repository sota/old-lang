#!/usr/bin/env python

import sys
sys.dont_write_bytecode = True

from subprocess import check_output, check_call

def task_submod_update():
    output = check_output('git submodule', shell=True)
    submods = [ line.split()[1] for line in output.strip().split('\n') ]
    for submod in submods:
        yield {
            'name': submod,
            'actions': ['git submodule update --init %(submod)s' % locals() ],
            'targets': [submod]
        }

def task_build_sota():
    python = 'python' if check_call('which pypy', shell=True) else 'pypy'
    python = 'python' # FIXME:  its slower; doing this for now ... -sai
    sotasrc = 'targetsota.py'
    rpython = 'repos/pypy/rpython/bin/rpython'
    return {
        'actions': ['%(python)s %(rpython)s %(sotasrc)s' % locals() ],
        'file_dep': [rpython],
        'targets': ['targetsota-c'],
    }
