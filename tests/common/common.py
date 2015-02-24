#!/usr/bin/env python

import os
import re
import sys

from subprocess import Popen, PIPE, CalledProcessError
from contextlib import contextmanager

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

def call(cmd, stdout=PIPE, stderr=PIPE, shell=True, nerf=False, verbose=False):
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
    if exitcode:
        raise CalledProcessError(exitcode, 'cmd=%(cmd)s; stdout=%(stdout)s; stderr=%(stderr)s' % locals() )
    return exitcode, stdout, stderr

