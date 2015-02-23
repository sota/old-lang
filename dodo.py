#!/usr/bin/env python

import sys
sys.dont_write_bytecode = True

from subprocess import check_output, PIPE

def task_updateinit():
    output = check_output('git submodule', shell=True)
    submods = [ line.split()[1] for line in output.strip().split('\n') ]
    for submod in submods:
        yield {
            'name': submod,
            'actions': ['git submodule update --init %(submod)s' % locals() ],
        }
