'''
utility to update version
'''
import re

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

