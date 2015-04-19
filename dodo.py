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
targetdir = 'src/target'
targetsrc = 'sota-interpreter.py'
sotadir = 'src/sota'
sotasrc = 'sota.c'
interpreter = 'sota-interpreter'
program = 'sota'
python = 'python' if call('which pypy', throw=False)[0] else 'pypy'
python = 'python' # FIXME:  its slower; doing this for now ... -sai
rpython = 'repos/pypy/rpython/bin/rpython'

PRE = 'tests/pre'
POST = 'tests/post'

def task_pyflakes():
    return {
        'actions': ['pyflakes %(targetsrc)s' % env() ],
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
            'src/sota/sota.c',
        ],
        'actions': ['cd src && tup', 'cp src/sota/sota .'],
        'targets': ['src/lexer/liblexer.a', 'sota'],
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

def task_target():
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
            '%(targetdir)s/%(targetsrc)s' % env(),
        ],
        'actions': [
            '%(python)s -B %(rpython)s --output %(interpreter)s %(targetdir)s/%(targetsrc)s' % env(),
        ],
        'targets': [interpreter],
        'clean': [clean_targets],
    }

def task_post():
    return {
        'verbosity': 2,
        'file_dep': [
            dodo,
            program,
            interpreter,
        ],
        'actions': ['py.test -v %(POST)s > %(POST)s/results' % env()],
        'targets': ['%(POST)s/results' % env()],
        'clean': [clean_targets],
    }

def task_success():
    return {
        'verbosity': 2,
        'file_dep': ['%(POST)s/results' % env()],
        'actions': [
            '%(sotadir)s/sota' % env(),
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
