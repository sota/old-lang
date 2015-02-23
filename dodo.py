#!/usr/bin/env python

import sys
sys.dont_write_bytecode = True

def task_hello():
    """hello py """

    def python_hello(times, text, targets):
        with open(targets[0], "a") as output:
            output.write(times * text)

    return {
        'actions': [(python_hello, [3, "py!\n"])],
        'targets': ["hello.txt"],
    }

def task_updateinit():
    return {
        'actions': ['git submodule update --init repos/*'],
        'targets': ['repos/pypy', 'repos/ragel'],
    } 
