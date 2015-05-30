#!/usr/bin/env python

import os
import re
import sys

SCRIPT_PATH, BASENAME = os.path.split(os.path.realpath(__file__) )
SCRIPT_NAME, SCRIPT_EXT = os.path.splitext(os.path.basename(BASENAME) )

from subprocess import check_call

def test_checksota():
    assert check_call(['./sota', '--help']) == 0
