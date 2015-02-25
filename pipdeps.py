#!/usr/bin/env python

import os
import re
import sys
sys.dont_write_bytecode = True

SCRIPT_PATH, BASENAME = os.path.split(os.path.realpath(__file__) )
SCRIPT_NAME, SCRIPT_EXT = os.path.splitext(os.path.basename(BASENAME) )
sys.path.insert(0, os.path.abspath(os.path.join(SCRIPT_PATH, 'utils') ) )

from common import cd, call, env

pipdeps = ['pyflakes', 'pytest']

def task_pip_install():
    for pipdep in pipdeps:
        yield {
            'name': pipdep,
            'actions': ['pip install --upgrade %(pipdep)s' % env()],
        }

