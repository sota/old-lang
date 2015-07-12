'''
shell utilities
'''
import os
import re
import fnmatch
from subprocess import Popen, PIPE, CalledProcessError
from contextlib import contextmanager

def expandpath(path):
    return os.path.realpath(os.path.expanduser(path))

def inversepath(path):
    return '/'.join(['..' for node in path.split('/')])

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
    for r, ds, fs in os.walk(os.path.dirname(pattern)):
        for f in fnmatch.filter(fs, os.path.basename(pattern)):
            matches.append(os.path.join(r, f) )
    return matches

