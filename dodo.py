#!/usr/bin/env python

import os
import re
import sys
sys.dont_write_bytecode = True

SCRIPT_PATH, BASENAME = os.path.split(os.path.realpath(__file__) )
SCRIPT_NAME, SCRIPT_EXT = os.path.splitext(os.path.basename(BASENAME) )
sys.path.insert(0, os.path.abspath(os.path.join(SCRIPT_PATH, 'src/utils') ) )

from common import cd, call, env
from doit.task import clean_targets

DOIT_CONFIG = { 'default_tasks': ['success'] }

dodo = 'dodo.py'
sota = 'sota'
ragel = 'src/ragel/ragel/ragel'
targetdir = 'src/jit'
targetsrc = 'sota.py'
sotadir = 'src/sota'
sotasrc = 'sota.cpp'
sotajit = 'sota-jit'
python = 'python' if call('which pypy', throw=False)[0] else 'pypy'
python = 'python' # FIXME:  its slower; doing this for now ... -sai
rpython = 'src/pypy/rpython/bin/rpython'

PRE = 'tests/pre'
POST = 'tests/post'

def submods():
    stdout = call('git submodule')[1].strip()
    return [line.split()[1] for line in stdout.split('\n')]

def task_pyflakes():
    return {
        'actions': ['pyflakes %(targetsrc)s' % env() ],
        'file_dep': [dodo],
    }

def task_submod():
    for submod in submods():
        yield {
            'name': submod,
            'verbosity': 2,
            'file_dep': [dodo],
            'actions': ['git submodule update --init %(submod)s' % env()],
            'targets': [os.path.join(submod, '.git')]
        }

def task_ragel():
    return {
        'verbosity': 2,
        'file_dep': [dodo, 'src/ragel/.git'],
        'actions': ['cd src/ragel && ./configure', 'cd src/ragel && make'],
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
            'src/cli/cli.cpp',
            'src/tclap/.git',
            'src/tclap/include/tclap/CmdLine.h',
        ],
        'actions': ['cd src && tup'],
        'targets': ['src/cli/test', 'src/lexer/test', 'src/lexer/lexer.cpp'],
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
            'src/cli/test',
            'src/lexer/test',
            'src/lexer/lexer.cpp',
            'src/pypy/.git',
            'src/ragel/.git',
            'src/argtable3/.git',
            '%(PRE)s/results' % env(),
            '%(targetdir)s/%(targetsrc)s' % env(),
        ],
        'actions': [
            '%(python)s -B %(rpython)s --output %(sota)s %(targetdir)s/%(targetsrc)s' % env(),
        ],
        'targets': [sota],
        'clean': [clean_targets],
    }

def task_post():
    return {
        'verbosity': 2,
        'file_dep': [
            dodo,
            sota,
        ],
        'actions': ['py.test -v %(POST)s > %(POST)s/results' % env()],
        'targets': ['%(POST)s/results' % env()],
        'clean': [clean_targets],
    }

def task_success():
    return {
        'file_dep': [sota, '%(POST)s/results' % env()],
        'actions': [
            './%(sota)s --help' % env(),
            'echo "sota build success!"',
        ],
    }

def task_tidy():

    for submod in submods():
        yield {
            'name': submod,
            'verbosity': 2,
            'actions': ['cd %(submod)s && git reset --hard HEAD && git clean -xfd' % env()],
        }
    yield {
        'name': 'sota/lang',
        'verbosity': 2,
        'actions': ['git clean -xfd'],
    }
