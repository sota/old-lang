'''
git utilities
'''

from shell import call

def subs2shas(path='.'):
    lines = call('cd %s && git submodule' % path)[1].strip().split('\n')
    return dict([(item[1],item[0]) for item in [line.split() for line in lines]])

