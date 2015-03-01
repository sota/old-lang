#!/usr/bin/env python

import os
import re
import sys
sys.dont_write_bytecode = True

SCRIPT_PATH, BASENAME = os.path.split(os.path.realpath(__file__) )
SCRIPT_NAME, SCRIPT_EXT = os.path.splitext(os.path.basename(BASENAME) )
sys.path.insert(0, os.path.abspath(os.path.join(SCRIPT_PATH, 'utils') ) )

from common import cd, call, env

dodo = 'dodo.py'
sota = 'sota'
sotasrc = 'targetsota.py'
python = 'python' if call('which pypy', throw=False)[0] else 'pypy'
python = 'python' # FIXME:  its slower; doing this for now ... -sai
rpython = 'repos/pypy/rpython/bin/rpython'

def task_pyflakes():
    return {
        'actions': ['pyflakes %(sotasrc)s' % env() ],
        'file_dep': [dodo],
    }

def task_submod_update():
    stdout = call('git submodule')[1]
    submods = [ line.split()[1] for line in stdout.strip().split('\n') ]
    for submod in submods:
        yield {
            'name': submod,
            'actions': ['git submodule update --init %(submod)s' % env() ],
            'file_dep': [dodo],
            'targets': [submod],
        }

def task_prebuild():
    return {
        'actions': ['py.test -v tests/pre > tests.prebuild'],
        'file_dep': [dodo, rpython],
        'targets': ['tests.prebuild'],
    }

def task_build_sota():
    return {
        'actions': ['%(python)s -B %(rpython)s %(sotasrc)s' % env(), 'mv targetsota-c sota'],
        'file_dep': [dodo, 'tests.prebuild', 'targetsota.py'],
        'targets': ['sota'],
    }

def task_postbuild():
    return {
        'actions': ['py.test -v tests/post > tests.postbuild'],
        'file_dep': [dodo, 'sota'],
        'targets': ['tests.postbuild'],
    }

def task_sota_build_success():
    return {
        'actions': ['echo "sota build success!"'],
        'file_dep': ['tests.postbuild'],
        'verbosity': 2,
    }
