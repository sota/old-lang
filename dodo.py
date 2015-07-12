#!/usr/bin/env python

import os
import sys
srcpath = os.path.abspath('src')
sys.path.insert(0, srcpath)
pythonpath = os.environ.get('PYTHONPATH', '')
pythonpath += ':' + srcpath
os.environ['PYTHONPATH'] = pythonpath
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'

from utils.git import subs2shas
from utils.shell import call, rglob
from utils.updater import SotaVersionUpdater
from utils.globalslocals import gl
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

submods = subs2shas().keys()
dodo = 'dodo.py'
sota = 'sota'
ragel = 'bin/ragel'
targetdir = 'src'
targetsrc = 'targetsota.py'
sotadir = 'src/sota'
sotasrc = 'sota.cpp'
sotajit = 'sota-jit'
python = 'python' if call('which pypy', throw=False)[0] else 'pypy'
python = 'python' # FIXME:  its slower; doing this for now ... -sai
rpython = 'src/pypy/rpython/bin/rpython'

versionh = 'src/cli/version.h'
versionpy = 'src/version.py'

CC = 'g++'
CXXFLAGS = '-Wall -Werror -O2 -std=c++11 -g -I../ -I../docopt.cpp'
PRE = 'tests/pre'
POST = 'tests/post'

try:
    SOTA_VERSION = open('VERSION').read().strip()
except:
    try:
        SOTA_VERSION = call('git describe')[1].strip()
    except:
        SOTA_VERSION = 'UNKNOWN'

def task_version():
    '''
    replace version strings in files
    '''
    for filename in [versionh, versionpy]:
        svu = SotaVersionUpdater(filename, SOTA_VERSION)
        yield {
            'name': filename,
            'actions': [svu.update],
            'targets': [filename],
            'clean': [clean_targets],
            'uptodate': [svu.uptodate],
        }

def task_unversion():
    '''
    undo version replacement with 'UNKNOWN'
    '''
    for filename in [versionh, versionpy]:
        svu = SotaVersionUpdater(filename, 'UNKNOWN')
        yield {
            'name': filename,
            'actions': [svu.update],
            'uptodate': [svu.uptodate],
        }

def task_pyflakes():
    '''
    run pyflakes on files
    '''
    for pyfile in rglob('%(targetdir)s/*.py' % gl()):
        yield {
            'name': pyfile,
            'actions': ['pyflakes ' + pyfile],
        }

def is_initd():
    return all([call('git config --get submodule.%s.url' % submod, throw=False)[1] for submod in submods])

def task_init():
    '''
    run git submodule init on submods
    '''
    return {
        'actions': ['git submodule init ' + ' '.join(submods)],
        'targets': ['.git/config'],
        'uptodate': [is_initd],
    }

def task_submod():
    '''
    run git submodule update on submods
    '''
    for submod in submods:
        yield {
            'name': submod,
            'file_dep': [dodo],
            'task_dep': ['init'],
            'actions': ['git submodule update %(submod)s' % gl()],
        }

def task_ragel():
    '''
    build ragel binary for use in build
    '''
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
    '''
    build libary for use as sota's commandline interface
    '''
    return {
        'file_dep': [dodo] + rglob('src/cli/*.{h,c,cpp}'),
        'task_dep': ['submod:src/docopt.cpp'],
        'actions': [
            'cd src/cli && %(CC)s %(CXXFLAGS)s -c ../docopt.cpp/docopt.cpp -o docopt.o' % gl(),
            'cd src/cli && %(CC)s %(CXXFLAGS)s -c cli.cpp -o cli.o' % gl(),
            'cd src/cli && ar crs libcli.a docopt.o cli.o',
            'cd src/cli && %(CC)s test.c libcli.a -o test' % gl(),
        ],
        'targets': ['src/cli/test', 'src/cli/libcli.a'],
        'clean': [clean_targets],
    }

def task_liblexer():
    '''
    build lexer library with ragel
    '''
    return {
        'file_dep': [dodo] + rglob('src/lexer/*.{h,rl,c}'),
        'task_dep': ['ragel'],
        'actions': [
            'cd src/lexer && ../ragel/ragel/ragel lexer.rl -o lexer.cpp',
            'cd src/lexer && %(CC)s %(CXXFLAGS)s -c lexer.cpp -o lexer.o' % gl(),
            'cd src/lexer && ar crs liblexer.a lexer.o',
            'cd src/lexer && %(CC)s test.c liblexer.a -o test' % gl(),
        ],
        'targets': ['src/lexer/lexer.cpp', 'src/lexer/test', 'src/lexer/liblexer.a'],
        'clean': [clean_targets],
    }

def task_pre():
    '''
    run pre tests
    '''
    return {
        'file_dep': [dodo],
        'actions': ['py.test -v %(PRE)s > %(PRE)s/results' % gl()],
        'targets': ['%(PRE)s/results' % gl()],
        'clean': [clean_targets],
    }

def task_sota():
    '''
    build sota program with rpython infrastructure
    '''
    return {
        'file_dep': [
            dodo,
            'src/cli/libcli.a',
            'src/lexer/liblexer.a',
        ] + rglob('%(targetdir)s/*.py' % gl()),
        'task_dep': ['submod:src/pypy', 'pre'],
        'actions': [
            '%(python)s -B %(rpython)s --output %(sota)s %(targetdir)s/%(targetsrc)s' % gl(),
        ],
        'targets': [sota],
        'clean': [clean_targets],
    }

def task_post():
    '''
    run post tests
    '''
    return {
        'file_dep': [dodo],
        'task_dep': ['sota'],
        'actions': ['py.test -v %(POST)s > %(POST)s/results' % gl()],
        'targets': ['%(POST)s/results' % gl()],
        'clean': [clean_targets],
    }

def task_success():
    '''
    run ./sota --help and print success
    '''
    return {
        'task_dep': ['sota', 'post'],
        'actions': [
            './%(sota)s --help > /dev/null 2>&1' % gl(),
            'echo "sota build success!"',
        ],
    }

def task_tidy():
    '''
    clean submods and sota/lang repo
    '''
    yield {
        'task_dep': ['unversion'],
        'name': 'sota/lang',
        'actions': ['git clean -xfd'],
    }
    for submod in submods:
        yield {
            'name': submod,
            'actions': [
                'cd %(submod)s && git reset --hard HEAD && git clean -xfd' % gl()
            ],
        }

