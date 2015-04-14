#!/usr/bin/env python

import os
import re
import sys
sys.dont_write_bytecode = True

SCRIPT_PATH, BASENAME = os.path.split(os.path.realpath(__file__) )
SCRIPT_NAME, SCRIPT_EXT = os.path.splitext(os.path.basename(BASENAME) )
sys.path.insert(0, os.path.abspath(os.path.join(SCRIPT_PATH, 'utils') ) )

from common import cd, call, env
from doit.task import clean_targets

DOIT_CONFIG = { 'default_tasks': ['success'] }

dodo = 'dodo.py'
sota = 'sota'
ragel = 'repos/ragel/ragel/ragel'
lexer_rl = 'src/lexer/lexer.rl'
lexer_c = 'src/lexer/lexer.c'
lexer_o = 'src/lexer/lexer.o'
liblexer_a = 'src/lexer/liblexer.a'
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

def task_submod():
    stdout = call('git submodule')[1]
    submods = [line.split()[1] for line in stdout.strip().split('\n')]
    for submod in submods:
        yield {
            'name': submod,
            'verbosity': 2,
            'file_dep': [dodo],
            'actions': ['git submodule update --init %(submod)s' % env() ],
            'targets': [os.path.join(submod, '.git')]
        }

def task_ragel():
    return {
        'verbosity': 2,
        'file_dep': [dodo, 'repos/ragel/.git'],
        'actions': ['cd repos/ragel && ./configure', 'cd repos/ragel && make'],
        'targets': [ragel],
        'clean': [clean_targets],
    }

def task_ccode():
    return {
        'verbosity': 2,
        'file_dep': [
            dodo,
            ragel,
            'src/lexer/lexer.h',
            'src/lexer/lexer.rl',
            'src/cli/cli.h',
            'src/cli/cli.c',
        ],
        'actions': ['cd src && tup'],
        'targets': ['src/lexer/liblexer.a', 'src/cli/libcli.a'],
        'clean': [clean_targets],
    }

def task_pre():
    return {
        'verbosity': 2,
        'file_dep': [dodo, rpython],
        'actions': ['py.test -v %(PRE)s > %(PRE)s/results' % env()],
        'targets': ['%(PRE)s/results' % env()],
        'clean': [clean_targets],
    }

def task_sota():
    return {
        'verbosity': 2,
        'file_dep': [
            dodo,
            ragel,
            liblexer_a,
            'repos/pypy/.git',
            'repos/ragel/.git',
            'repos/argtable3/.git',
            '%(PRE)s/results' % env(),
            'targetsota.py',
        ],
        'actions': [
            '%(python)s -B %(rpython)s %(sotasrc)s' % env(),
            'mv targetsota-c sota'
        ],
        'targets': ['sota'],
        'clean': [clean_targets],
    }

def task_post():
    return {
        'verbosity': 2,
        'file_dep': [dodo, 'sota'],
        'actions': ['py.test -v %(POST)s > %(POST)s/results' % env()],
        'targets': ['%(POST)s/results' % env()],
        'clean': [clean_targets],
    }

def task_success():
    return {
        'verbosity': 2,
        'file_dep': ['%(POST)s/results' % env()],
        'actions': [
            './sota',
            'echo "sota build success!"',
        ],
    }

def task_tidy():
    return {
        'verbosity': 2,
        'actions': [
            'git clean -xfd',
            'cd repos/pypy && git reset --hard HEAD && git clean -xfd',
            'cd repos/ragel && git reset --hard HEAD && git clean -xfd',
            'cd repos/argtable3 && git reset --hard HEAD && git clean -xfd',
        ],
    }
