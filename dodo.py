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

def version_changed():
    try:
        return open(versionh).read().strip() == VERSIONH
    except:
        pass
    return False

def task_version():
    return {
        'actions': [
            "echo '%(VERSIONH)s' > %(versionh)s" % env()
        ],
        'targets': [versionh],
        'clean': [clean_targets],
        'uptodate': [version_changed],
    }

def task_pyflakes():
    return {
        'file_dep': [dodo],
        'actions': ['pyflakes %(targetsrc)s' % env()],
    }

def task_submod():
    for submod in submods():
        shafile = submod + '-sha'
        inverse = inversepath(submod)
        yield {
            'name': submod,
            'file_dep': [dodo],
            'actions': [
                'git submodule update --init %(submod)s' % env(),
                'cd %(submod)s && git rev-parse HEAD > %(inverse)s/%(shafile)s' % env(),
            ],
            'targets': [shafile],
        }

def task_ragel():
    return {
        'file_dep': [dodo, 'src/ragel-sha'],
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
        'file_dep': [
            dodo,
            versionh,
            'src/tclap-sha',
        ] + rglob('src/cli/*.{h,c,cpp}'),
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
        'file_dep': [
            dodo,
            ragel,
        ] + rglob('src/lexer/*.{h,rl,c}'),
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
        'file_dep': [
            dodo,
        ],
        'actions': ['py.test -v %(PRE)s > %(PRE)s/results' % env()],
        'targets': ['%(PRE)s/results' % env()],
        'clean': [clean_targets],
    }

def task_sota():
    return {
        'file_dep': [
            dodo,
            'src/cli/test',
            'src/lexer/test',
            'src/pypy-sha',
            'src/ragel-sha',
            '%(PRE)s/results' % env(),
        ] + rglob('%(targetdir)s/*.py' % env()) + rglob('src/lexer/*.{h,rl}') + rglob('src/cli/*.{h,cpp}'),
        'actions': [
            '%(python)s -B %(rpython)s --output %(sota)s %(targetdir)s/%(targetsrc)s' % env(),
        ],
        'targets': [sota],
        'clean': [clean_targets],
    }

def task_post():
    return {
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

