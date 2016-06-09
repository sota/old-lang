#!/usr/bin/env python

import os
import sys
import glob
import json

SRCPATH = os.path.abspath('src')
sys.path.insert(0, SRCPATH)
PYTHONPATH = os.environ.get('PYTHONPATH', '')
PYTHONPATH += ':' + SRCPATH
os.environ['PYTHONPATH'] = PYTHONPATH
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'

from utils.git import subs2shas
from utils.shell import call, rglob
from utils.writer import SotaVersionWriter
from utils.globalslocals import gl
from doit.task import clean_targets

DOIT_CONFIG = {
    'verbosity': 2,
    'default_tasks': ['success'],
}

REPO = os.path.dirname(__file__)
SUBMODS = subs2shas().keys()
DODO = 'dodo.py'
COLM = 'bin/colm'
RAGEL = 'bin/ragel'
TARGETDIR = 'src'
TARGETSRC = 'targetsota.py'
PYTHON = 'python' if call('which pypy', throw=False)[0] else 'pypy'
PYTHON = 'python' # FIXME:  its slower; doing this for now ... -sai pylint: disable=fixme
RPYTHON = 'src/pypy/rpython/bin/rpython'
ROOTDIR = 'root'
BINDIR = '%(ROOTDIR)s/bin' % gl()
LIBDIR = '%(ROOTDIR)s/lib' % gl()
PREDIR = 'tests/pre'
POSTDIR = 'tests/post'

VERSION_JSON = 'src/version.json'

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
    create version files from version.json template
    '''
    versionfiles = json.load(open(VERSION_JSON))
    for filename, contents in versionfiles.iteritems():
        svw = SotaVersionWriter(filename, contents % globals())
        yield {
            'name': filename,
            'actions': [svw.update],
            'uptodate': [svw.uptodate],
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

def task_colm():
    '''
    build colm binary for use in build
    '''
    return {
        'file_dep': [DODO],
        'task_dep': ['pre', 'submod:src/colm'],
        'actions': [
            'cd src/colm && ./autogen.sh',
            'cd src/colm && ./configure --prefix=%(REPO)s' % gl(),
            'cd src/colm && make && make install',
        ],
        'targets': [COLM],
        'clean': [clean_targets],
    }

def task_ragel():
    '''
    build colm binary for use in build
    '''
    return {
        'file_dep': [DODO],
        'task_dep': ['pre', 'colm'],
        'actions': [
            'cd src/ragel && ./autogen.sh',
            'cd src/ragel && ./configure --prefix=%(REPO)s --disable-manual' % gl(),
            'cd src/ragel && make && make install',
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
            'cd src/cli && make -j %(J)s' % gl(),
            'install -C -D src/cli/libcli.so %(LIBDIR)s/libcli.so' % gl(),
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
        'task_dep': ['pre', 'ragel', 'version:src/version.h'],
        'actions': [
            'cd src/lexer && make -j %(J)s RAGEL=%(REPO)s/%(RAGEL)s' % gl(),
            'install -C -D src/lexer/liblexer.so %(LIBDIR)s/liblexer.so' % gl(),
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
            'task_dep': ['submod', 'version:src/version.py'],
            'actions': [(covcmd if hastests(pyfile) else msgcmd) % gl()],
        }

def task_pylint():
    '''
    run pylint on all pyfiles
    '''
    excludes = ['src/doit/dodo.py']
    for pyfile in globs('*.py', 'src/*/*.py', '%(PREDIR)s/*/*.py' % gl()) - globs(*excludes):
        yield {
            'name': pyfile,
            'task_dep': ['submod', 'version:src/version.py'],
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

