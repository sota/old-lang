'''
utilies with globals and locals
'''
import inspect

def gl():
    '''
    returns dict of globals merged with locals
    '''
    try:
        frame = inspect.currentframe().f_back
        return dict(frame.f_globals.items() + frame.f_locals.items() )
    finally:
        del frame

