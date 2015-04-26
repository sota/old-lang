#!/usr/bin/env python

import os
import re
import sys

SCRIPT_PATH, BASENAME = os.path.split(os.path.realpath(__file__) )
SCRIPT_NAME, SCRIPT_EXT = os.path.splitext(os.path.basename(BASENAME) )
sys.path.insert(0, os.path.abspath(os.path.join(SCRIPT_PATH, '../../src/utils') ) )

from common import cd, call

def test_checksotajit():
    assert call('./sota-jit hello')[0] == 0
