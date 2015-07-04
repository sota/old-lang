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

def subs2shas(path='.'):
    lines = call('cd %s && git submodule' % path)[1].strip().split('\n')
    return dict([(item[1],item[0]) for item in [line.split() for line in lines]])

def ini2dict(ini):
    config = {}
    try:
        from ConfigParser import SafeConfigParser
        parser = SafeConfigParser()
        parser.read(ini)
        for section in parser.sections():
            config[section] = {}
            for option in parser.options(section):
                config[section][option] = parser.get(section, option)
    except: pass
    return config

#src: http://stackoverflow.com/questions/7204805/dictionaries-of-dictionaries-merge
def merge(a, b):
    """merges b into a and return merged result

    NOTE: tuples and arbitrary objects are not handled as it is totally ambiguous what should happen"""

    class MergeError(Exception):
        pass

    if b:
        key = None
        try:
            if isscalar(a):
                # border case for first run or if a is a primitive
                a = b
            elif islist(a):
                # lists can be only appended
                if islist(b):
                    # merge lists
                    a.extend(b)
                else:
                    # append to list
                    a.append(b)
            elif isdict(a):
                # dicts must be merged
                if isdict(b):
                    for key in b:
                        if key in a:
                            a[key] = merge(a[key], b[key])
                        else:
                            a[key] = b[key]
                else:
                    raise MergeError('Cannot merge non-dict "%s" into dict "%s"' % (b, a))
            else:
                raise MergeError('NOT IMPLEMENTED "%s" into "%s"' % (b, a))
        except TypeError, e:
            raise MergeError('TypeError "%s" in key "%s" when merging "%s" into "%s"' % (e, key, b, a))
    return a

class SotaVersionUpdater(object):
    def __init__(self, filename, version):
        self.filename = filename
        self.version = version
        self.pattern = '''(.*SOTA_VERSION += +["'])([\w\-\.]+)(["'])'''
        self.regex = re.compile(self.pattern)
        self.replace = r'\1' + version + r'\3'
        self.contents = open(filename).read()
    def uptodate(self):
        match = self.regex.search(self.contents)
        if match:
            return match.group(2) == self.version
        return False
    def update(self):
        updated = self.regex.sub(self.replace, self.contents)
        if not updated:
            raise Exception('VersionUpdater.update produced empty updated string')
        with open(self.filename, 'w') as f:
            f.write(updated)

