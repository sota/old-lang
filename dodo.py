#!/usr/bin/env python

import os
import re
import sys
sys.dont_write_bytecode = True

SCRIPT_PATH, BASENAME = os.path.split(os.path.realpath(__file__) )
SCRIPT_NAME, SCRIPT_EXT = os.path.splitext(os.path.basename(BASENAME) )
sys.path.insert(0, os.path.abspath(os.path.join(SCRIPT_PATH, 'utils') ) )

from common import cd, call, env

DOIT_CONFIG = { 'default_tasks': ['success'] }

dodo = 'dodo.py'
sota = 'sota'
sotasrc = 'targetsota.py'
python = 'python' if call('which pypy', throw=False)[0] else 'pypy'
python = 'python' # FIXME:  its slower; doing this for now ... -sai
rpython = 'repos/pypy/rpython/bin/rpython'

PRE = 'tests/pre'
POST = 'tests/post'

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
            'file_dep': [dodo],
            'actions': ['git submodule update --init %(submod)s' % env() ],
            'targets': ['%(submod)s/.git' % env()],
            'targets': [os.path.join(submod, '.git')]
        }

def task_build_ragel():
    return {
        'file_dep': [dodo, 'repos/ragel/.git'],
        'actions': ['cd repos/ragel && ./configure', 'cd repos/ragel && make'],
        'targets': ['repos/ragel/ragel/ragel'],
    }

def task_prebuild():
    return {
        'file_dep': [dodo, rpython],
        'actions': ['py.test -v %(PRE)s > %(PRE)s/results' % env()],
        'targets': ['%(PRE)s/results' % env()],
    }

def task_build_sota():
    return {
        'file_dep': [
            dodo,
            'repos/pypy/.git',
            'repos/ragel/.git',
            '%(PRE)s/results' % env(),
            'targetsota.py',
            'repos/ragel/ragel/ragel',
        ],
        'actions': [
            '%(python)s -B %(rpython)s %(sotasrc)s' % env(),
            'mv targetsota-c sota'
        ],
        'targets': ['sota'],
    }

def task_postbuild():
    return {
        'file_dep': [dodo, 'sota'],
        'actions': ['py.test -v %(POST)s > %(POST)s/results' % env()],
        'targets': ['%(POST)s/results' % env()],
    }

def task_success():
    return {
        'file_dep': ['%(POST)s/results' % env()],
        'actions': ['echo "sota build success!"'],
        'verbosity': 2,
    }

def task_tidy():
    return {
        'actions': [
            'git clean -xfd',
            'cd repos/pypy && git reset --hard HEAD && git clean -xfd',
            'cd repos/ragel && git reset --hard HEAD && git clean -xfd',
        ],
        'verbosity': 2,
    }
