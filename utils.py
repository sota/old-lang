#!/usr/bin/env python

import os
import re
import sys
import inspect

from subprocess import Popen, PIPE, CalledProcessError
from contextlib import contextmanager
from types import ModuleType, FunctionType, GeneratorType

def isstr(obj):
    return isinstance(obj, str)

def isunicode(obj):
    return isinstance(obj, unicode)

def isint(obj):
    return isinstance(obj, int)

def islong(obj):
    return isinstance(obj, long)

def isfloat(obj):
    return isinstance(obj, float)

def ismodule(obj):
    return isinstance(obj, ModuleType)

def isfunction(obj):
    return isinstance(obj, FunctionType)

def isgenerator(obj):
    return isinstance(obj, GeneratorType)

def isscalar(obj):
    return  obj is None or \
            isstr(obj) or \
            isunicode(obj) or \
            isint(obj) or \
            islong(obj) or \
            isfloat(obj)

def islist(obj):
    return isinstance(obj, list)

def isdict(obj):
    return isinstance(obj, dict)

def expand(obj, env):
    if isstr(obj):
        return obj % env
    elif islist(obj):
        return [expand(i, env) for i in obj]
    elif isdict(obj):
        return dict([(k,expand(v, env)) for k,v in obj.iteritems()])
    elif isscalar(obj):
        return obj
    raise Exception('expand: obj != str, list, dict')

def commalist(obj):
    if isstr(obj):
        if ',' in obj:
            return obj.split(',')
        return [obj]
    return obj

def expandpath(path):
    return os.path.realpath(os.path.expanduser(path))

def inversepath(path):
    return '/'.join(['..' for node in path.split('/')])

def filterargs(*kwargs):
    return filter(lambda arg: not any(map(lambda kwarg: arg.startswith(kwarg+'='), kwargs)), sys.argv[1:])

@contextmanager
def cd(*args, **kwargs):
    mkdir = kwargs.pop('mkdir', True)
    verbose = kwargs.pop('verbose', False)
    path = os.path.sep.join(args)
    path = os.path.normpath(path)
    path = os.path.expanduser(path)
    prev = os.getcwd()
    if path != prev:
        if mkdir:
            call('mkdir -p %(path)s' % locals(), verbose=verbose)
        os.chdir(path)
        curr = os.getcwd()
        sys.path.append(curr)
        if verbose:
            print 'cd %s' % curr
    try:
        yield
    finally:
        if path != prev:
            sys.path.remove(curr)
            os.chdir(prev)
            if verbose:
                print 'cd %s' % prev

def call(cmd, stdout=PIPE, stderr=PIPE, shell=True, nerf=False, throw=True, verbose=False):
    if verbose or nerf:
        print cmd
    if nerf:
        return (None, 'nerfed', 'nerfed')
    process = Popen(cmd, stdout=stdout, stderr=stderr, shell=shell)
    stdout, stderr = process.communicate()
    exitcode = process.poll()
    if verbose:
        if stdout:
            print stdout
        if stderr:
            print stderr
    if throw and exitcode:
        raise CalledProcessError(exitcode, 'cmd=%(cmd)s; stdout=%(stdout)s; stderr=%(stderr)s' % locals() )
    return exitcode, stdout, stderr

def env():
    try:
        frame = inspect.currentframe().f_back
        return dict(frame.f_globals.items() + frame.f_locals.items() )
    finally:
        del frame

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

def parameterized(d):
    ''' d for decorator f for function '''
    def layer(*args, **kwargs):
        def repl(f):
            return d(f, *args, **kwargs)
        return repl
    return layer

def timed(func):
    def wrap_func(*args, **kwargs):
        def prepend_time(result):
            result['actions'] = ['time ' + action for action in result.get('actions', [])]
            return result
        results = func(*args, **kwargs)
        if isgenerator(results):
            def wrap_gen(func):
                for result in results:
                    yield prepend_time(result)
            return wrap_gen(func)
        else:
            def wrap_reg(func):
                return prepend_time(results)
            return wrap_reg(func)
    return wrap_func

def get_subs2shas():
    lines = call('git submodule')[1].strip().split('\n')
    return dict([(item[1],item[0]) for item in [line.split() for line in lines]])
