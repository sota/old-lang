'''
utility for writing version files
'''

import os

class SotaVersionWriter(object):
    def __init__(self, filename, contents):
        assert filename
        assert contents
        self.filename = filename
        self.contents = contents
    def uptodate(self):
        if os.path.isfile(self.filename):
            return self.contents == open(self.filename).read()
        return False
    def update(self):
        with open(self.filename, 'w') as f:
            f.write(self.contents)
