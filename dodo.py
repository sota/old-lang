#!/usr/bin/env python

import os
import re
import sys
sys.dont_write_bytecode = True

SCRIPT_PATH, BASENAME = os.path.split(os.path.realpath(__file__) )
SCRIPT_NAME, SCRIPT_EXT = os.path.splitext(os.path.basename(BASENAME) )

from utils import cd, call, env, inversepath
from doit.task import clean_targets

from doit.reporter import ConsoleReporter
class MyReporter(ConsoleReporter):
    def execute_task(self, task):
        self.outstream.write('MyReporter --> %s\n' % task.title())

DOIT_CONFIG = {
    'verbosity': 2,
    'default_tasks': ['success'],
    #'reporter': MyReporter,
}

versionh = 'src/version.h'
dodo = 'dodo.py'
sota = 'sota'
ragel = 'bin/ragel'
targetdir = 'src/jit'
targetsrc = 'sota.py'
sotadir = 'src/sota'
sotasrc = 'sota.cpp'
sotajit = 'sota-jit'
python = 'python' if call('which pypy', throw=False)[0] else 'pypy'
python = 'python' # FIXME:  its slower; doing this for now ... -sai
rpython = 'src/pypy/rpython/bin/rpython'

CC = 'g++'
CXXFLAGS = '-Wall -Werror -O2 -std=c++11 -g -I../ -I../tclap/include'
PRE = 'tests/pre'
POST = 'tests/post'

try:
    VERSION = open('VERSION').read().strip()
except:
    try:
        VERSION = call('git describe')[1].strip()
    except:
        VERSION = 'UNKNOWN'

VERSIONH = '''
#ifndef __SOTA_VERSION__
#define __SOTA_VERSION__ = 1

#include <string>
const std::string VERSION = "%(VERSION)s";

#endif /*__SOTA_VERSION__*/
''' % env()
VERSIONH = VERSIONH.strip()

def rglob(pattern):
    matches = []
    # support for shell-like {x,y} syntax
    regex = re.compile('(.*){(.*)}(.*)')
    match = regex.search(pattern)
    if match:
        prefix, alternates, suffix = match.groups()
        for alternate in alternates.split(','):
            matches += rglob(prefix + alternate.strip() + suffix)
        return matches
    # support for recursive glob
    import fnmatch
    for r, ds, fs in os.walk(os.path.dirname(pattern)):
        for f in fnmatch.filter(fs, os.path.basename(pattern)):
            matches.append(os.path.join(r, f) )
    return matches

def submods():
    stdout = call('git submodule')[1].strip()
    return [line.split()[1] for line in stdout.split('\n')]

def version_unchanged():
    try:
        return open(versionh).read().strip() == VERSIONH
    except:
        pass
    return False

def task_version():
    return {
        'actions': ["echo '%(VERSIONH)s' > %(versionh)s" % env()],
        'targets': [versionh],
        'clean': [clean_targets],
        'uptodate': [version_unchanged],
    }

def task_pyflakes():
    return {
        'file_dep': [dodo],
        'actions': ['pyflakes %(targetsrc)s' % env()],
    }

def task_init():
    return {
        'actions': ['git submodule init ' + ' '.join(submods())],
        'targets': ['.git/config'],
    }

def task_submod():
    for submod in submods():
        shafile = submod + '-sha'
        inverse = inversepath(submod)
        yield {
            'name': submod,
            'file_dep': [dodo],
            'task_dep': ['init'],
            'actions': ['git submodule update %(submod)s' % env()],
            'targets': [shafile],
        }

def task_ragel():
    return {
        'file_dep': [dodo],
        'task_dep': ['submod:src/ragel'],
        'actions': [
            'cd src/ragel && ./configure --prefix='+os.getcwd(),
            'cd src/ragel && make',
            'cd src/ragel && make install',
        ],
        'targets': [ragel],
        'clean': [clean_targets],
    }

def task_libcli():
    return {
        'file_dep': [dodo] + rglob('src/cli/*.{h,c,cpp}'),
        'task_dep': ['version', 'submod:src/tclap'],
        'actions': [
            'cd src/cli && %(CC)s %(CXXFLAGS)s -c cli.cpp -o cli.o' % env(),
            'cd src/cli && ar crs libcli.a cli.o',
            'cd src/cli && %(CC)s test.c libcli.a -o test' % env(),
        ],
        'targets': ['src/cli/test', 'src/cli/libcli.a'],
        'clean': [clean_targets],
    }

def task_liblexer():
    return {
        'file_dep': [dodo] + rglob('src/lexer/*.{h,rl,c}'),
        'task_dep': ['ragel'],
        'actions': [
            'cd src/lexer && ../ragel/ragel/ragel lexer.rl -o lexer.cpp',
            'cd src/lexer && %(CC)s %(CXXFLAGS)s -c lexer.cpp -o lexer.o' % env(),
            'cd src/lexer && ar crs liblexer.a lexer.o',
            'cd src/lexer && %(CC)s test.c liblexer.a -o test' % env(),
        ],
        'targets': ['src/lexer/lexer.cpp', 'src/lexer/test', 'src/lexer/liblexer.a'],
        'clean': [clean_targets],
    }

def task_pre():
    return {
        'file_dep': [dodo],
        'actions': ['py.test -v %(PRE)s > %(PRE)s/results' % env()],
        'targets': ['%(PRE)s/results' % env()],
        'clean': [clean_targets],
    }

def task_sota():
    return {
        'file_dep': [dodo] + rglob('%(targetdir)s/*.py' % env()),
        'task_dep': ['libcli', 'liblexer', 'submod:src/pypy', 'pre'],
        'actions': [
            '%(python)s -B %(rpython)s --output %(sota)s %(targetdir)s/%(targetsrc)s' % env(),
        ],
        'targets': [sota],
        'clean': [clean_targets],
    }

def task_post():
    return {
        'file_dep': [dodo],
        'task_dep': ['sota'],
        'actions': ['py.test -v %(POST)s > %(POST)s/results' % env()],
        'targets': ['%(POST)s/results' % env()],
        'clean': [clean_targets],
    }

def task_success():
    return {
        'task_dep': ['sota', 'post'],
        'actions': [
            './%(sota)s --help > /dev/null 2>&1' % env(),
            'echo "sota build success!"',
        ],
    }

def task_tidy():

    for submod in submods():
        yield {
            'name': submod,
            'actions': [
                'cd %(submod)s && git reset --hard HEAD && git clean -xfd' % env()
            ],
        }
    yield {
        'name': 'sota/lang',
        'actions': ['git clean -xfd'],
    }

