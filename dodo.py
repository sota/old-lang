#!/usr/bin/env python

import os
import sys
sys.dont_write_bytecode = True

SCRIPT_PATH, BASENAME = os.path.split(os.path.realpath(__file__) )
SCRIPT_NAME, SCRIPT_EXT = os.path.splitext(os.path.basename(BASENAME) )
sys.path.insert(0, 'src')

from utils import *
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

doitinid = {}
merge(doitinid, ini2dict('doit.ini').get('doit'))
merge(doitinid, ini2dict(expandpath(doitinid.get('doitini',{}))).get('doit'))
submods = subs2shas().keys()
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
CXXFLAGS = '-Wall -Werror -O2 -std=c++11 -g -I../ -I../docopt.cpp'
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
    for pyfile in rglob('%(targetdir)s/*.py' % env()):
        yield {
            'name': pyfile,
            'actions': ['pyflakes ' + pyfile],
        }

def is_initd():
    return all([call('git config --get submodule.%s.url' % submod, throw=False)[1] for submod in submods])

def task_init():
    return {
        'actions': ['git submodule init ' + ' '.join(submods)],
        'targets': ['.git/config'],
        'uptodate': [is_initd],
    }

def task_submod():
    for submod in submods:
        yield {
            'name': submod,
            'file_dep': [dodo],
            'task_dep': ['init'],
            'actions': ['git submodule update %(submod)s' % env()],
        }

def task_ragel():
    return {
        'file_dep': [dodo],
        'task_dep': ['submod:src/ragel'],
        'actions': [
            'cd src/ragel && ./autogen.sh',
            'cd src/ragel && ./configure --prefix='+os.getcwd(),
            'cd src/ragel && make',
            'cd src/ragel && make install',
        ],
        'targets': [ragel],
        'clean': [clean_targets],
    }

def task_libcli():
    return {
        'file_dep': [dodo, versionh] + rglob('src/cli/*.{h,c,cpp}'),
        'task_dep': ['submod:src/docopt.cpp'],
        'actions': [
            'cd src/cli && %(CC)s %(CXXFLAGS)s -c ../docopt.cpp/docopt.cpp -o docopt.o' % env(),
            'cd src/cli && %(CC)s %(CXXFLAGS)s -c cli.cpp -o cli.o' % env(),
            'cd src/cli && ar crs libcli.a docopt.o cli.o',
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
        'file_dep': [
            dodo,
            'src/cli/libcli.a',
            'src/lexer/liblexer.a',
        ] + rglob('%(targetdir)s/*.py' % env()),
        'task_dep': ['submod:src/pypy', 'pre'],
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

def task_show():
    def show():
        keywidth = max(map(lambda k: len(k), doitinid.keys())) + 4
        valwidth = max(map(lambda v: len(v), doitinid.values()))
        for key, val in doitinid.iteritems():
            print key.ljust(keywidth), '=', val.ljust(valwidth)
    return {
        'actions': [show],
    }

def task_tidy():

    for submod in submods:
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

