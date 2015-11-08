#!/usr/bin/env python

import os
import sys
import glob
SRCPATH = os.path.abspath('src')
sys.path.insert(0, SRCPATH)
PYTHONPATH = os.environ.get('PYTHONPATH', '')
PYTHONPATH += ':' + SRCPATH
os.environ['PYTHONPATH'] = PYTHONPATH
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'

from utils.git import subs2shas
from utils.shell import call, rglob
from utils.updater import SotaVersionUpdater
from utils.globalslocals import gl
from doit.task import clean_targets

DOIT_CONFIG = {
    'verbosity': 2,
    'default_tasks': ['success'],
}

SUBMODS = subs2shas().keys()
DODO = 'dodo.py'
RAGEL = 'src/ragel/bin/ragel'
TARGETDIR = 'src'
TARGETSRC = 'targetsota.py'
PYTHON = 'python' if call('which pypy', throw=False)[0] else 'pypy'
PYTHON = 'python' # FIXME:  its slower; doing this for now ... -sai pylint: disable=fixme
RPYTHON = 'src/pypy/rpython/bin/rpython'
BINDIR = 'root/bin'
LIBDIR = 'root/lib'
PREDIR = 'tests/pre'
POSTDIR = 'tests/post'

VERSIONH = 'src/cli/version.h'
VERSIONPY = 'src/version.py'

CC = os.getenv('CXX', 'g++')
CXXFLAGS = '-Wall -Werror -fPIC -O2 -std=c++11 -g -I../ -I../docopt'

ENVS = [
    'PYTHONPATH=.:src:src/pypy:$PYTHONPATH',
]
ENVS = ' '.join(ENVS)

try:
    J = call('nproc')[1].strip()
except: #pylint: disable=bare-except
    J = 1

try:
    SOTA_VERSION = open('VERSION').read().strip()
except: #pylint: disable=bare-except
    try:
        SOTA_VERSION = call('git describe')[1].strip()
    except: #pylint: disable=bare-except
        SOTA_VERSION = 'UNKNOWN'

def globs(*paths):
    '''
    returns a set of all paths glob-matched
    '''
    return set([item for item in [glob.glob(path) for path in paths] for item in item])

def task_version():
    '''
    replace version strings in files
    '''
    for filename in [VERSIONH, VERSIONPY]:
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
    for filename in [VERSIONH, VERSIONPY]:
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
    for pyfile in rglob('%(TARGETDIR)s/*.py' % gl()):
        yield {
            'name': pyfile,
            'actions': ['pyflakes ' + pyfile],
        }

def is_initd():
    return all([call('git config --get submodule.%s.url' % submod, throw=False)[1] for submod in SUBMODS])

def task_init():
    '''
    run git submodule init on submods
    '''
    return {
        'actions': ['git submodule init ' + ' '.join(SUBMODS)],
        'targets': ['.git/config'],
        'uptodate': [is_initd],
    }

def task_submod():
    '''
    run git submodule update on submods
    '''
    for submod in SUBMODS:
        yield {
            'name': submod,
            'file_dep': [DODO],
            'task_dep': ['init'],
            'actions': ['git submodule update %(submod)s' % gl()],
        }

def task_ragel():
    '''
    build ragel binary for use in build
    '''
    target = 'bin/rlhc' if os.environ.get('RAGEL') in ('7', '70') else 'bin/ragel'
    return {
        'file_dep': [DODO],
        'task_dep': ['pre', 'submod:src/ragel'],
        'actions': [
            'cd src/ragel && make -j %(J)s %(target)s' % gl(),
        ],
        'targets': [RAGEL],
        'clean': [clean_targets],
    }

def task_libcli():
    '''
    build so libary for use as sota's commandline interface
    '''
    return {
        'file_dep': [DODO] + rglob('src/cli/*.{h,c,cpp}'),
        'task_dep': ['pre', 'submod:src/docopt'],
        'actions': [
            'mkdir -p %(LIBDIR)s' % gl(),
            'cd src/cli && %(CC)s %(CXXFLAGS)s -c ../docopt/docopt.cpp -o docopt.o' % gl(),
            'cd src/cli && %(CC)s %(CXXFLAGS)s -c cli.cpp -o cli.o' % gl(),
            'cd src/cli && %(CC)s -shared -o ../../%(LIBDIR)s/libcli.so docopt.o cli.o' % gl(),
            'cd src/cli && %(CC)s -Wall test.c -L../../%(LIBDIR)s -lcli -o test' % gl(),
        ],
        'targets': ['src/cli/test', '%(LIBDIR)s/libcli.so' % gl()],
        'clean': [clean_targets],
    }

def task_liblexer():
    '''
    build lexer library with ragel
    '''
    return {
        'file_dep': [DODO] + rglob('src/lexer/*.{h,rl,c}'),
        'task_dep': ['pre', 'ragel'],
        'actions': [
            'mkdir -p %(LIBDIR)s' % gl(),
            'cd src/lexer && ../../%(RAGEL)s lexer.rl -o lexer.cpp' % gl(),
            'cd src/lexer && %(CC)s %(CXXFLAGS)s -c lexer.cpp -o lexer.o' % gl(),
            'cd src/lexer && %(CC)s -shared -o ../../%(LIBDIR)s/liblexer.so lexer.o' % gl(),
            'cd src/lexer && %(CC)s -Wall test.c -L../../%(LIBDIR)s -llexer -o test' % gl(),
        ],
        'targets': ['src/lexer/lexer.cpp', 'src/lexer/test', '%(LIBDIR)s/liblexer.so' % gl()],
        'clean': [clean_targets],
    }

def task_pytest():
    '''
    run 'py.test --verbose %(PREDIR)s
    ''' % gl()
    return {
        'task_dep': ['submod'],
        'actions': ['py.test -s -vv %(PREDIR)s > %(PREDIR)s/results' % gl()],
    }

def task_pycov():
    '''
    run 'py.test --cov=<pyfile> %(PREDIR)s/<pyfile>'
    ''' % gl()
    def hastests(pyfile):
        return os.path.exists(os.path.join(PREDIR, pyfile))
    excludes = ['dodo.py']
    pyfiles = globs('src/*/*.py') - globs(*excludes)
    for pyfile in sorted(pyfiles, key=hastests):
        covcmd = 'py.test -s -vv --cov=%(pyfile)s %(PREDIR)/%(pyfile)s'
        msgcmd = 'echo "no tests found (%(PREDIR)s/%(pyfile)s to run coverage on %(pyfile)s"'
        yield {
            'name': pyfile,
            'task_dep': ['submod'],
            'actions': [(covcmd if hastests(pyfile) else msgcmd) % gl()],
        }

def task_pylint():
    '''
    run pylint on all pyfiles
    '''
    excludes = []
    for pyfile in globs('*.py', 'src/*/*.py', '%(PREDIR)s/*/*.py' % gl()) - globs(*excludes):
        yield {
            'name': pyfile,
            'task_dep': ['submod'],
            'actions': ['%(ENVS)s pylint -E -j4 --rcfile %(PREDIR)s/pylint.rc %(pyfile)s' % gl()],
        }

def task_pre():
    '''
    run pre tests: pytest, pycov and pylint
    '''
    return {
        'task_dep': ['pytest', 'pycov', 'pylint'],
        'actions': ['echo "sota pre tests successfully tested!"'],
    }

def task_sota():
    '''
    build sota program with rpython infrastructure
    '''
    return {
        'file_dep': [
            DODO,
            '%(LIBDIR)s/libcli.so' % gl(),
            '%(LIBDIR)s/liblexer.so' % gl(),
        ] + rglob('%(TARGETDIR)s/*.py' % gl()),
        'task_dep': ['submod:src/pypy', 'pre'],
        'actions': [
            'mkdir -p %(BINDIR)s' % gl(),
            '%(PYTHON)s -B %(RPYTHON)s --output %(BINDIR)s/sota %(TARGETDIR)s/%(TARGETSRC)s' % gl(),
        ],
        'targets': ['%(BINDIR)s/sota' % gl()],
        'clean': [clean_targets],
    }

def task_post():
    '''
    run post tests
    '''
    return {
        'file_dep': [DODO],
        'task_dep': ['sota'],
        'actions': [
            'py.test -s -vv %(POSTDIR)s > %(POSTDIR)s/results' % gl(),
        ],
        'targets': ['%(POSTDIR)s/results' % gl()],
        'clean': [clean_targets],
    }

def task_success():
    '''
    run ./sota --help and print success
    '''
    return {
        'task_dep': ['sota', 'post'],
        'actions': [
            './sota --help > /dev/null 2>&1' % gl(),
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
    for submod in SUBMODS:
        yield {
            'name': submod,
            'actions': [
                'cd %(submod)s && git reset --hard HEAD && git clean -xfd' % gl()
            ],
        }

