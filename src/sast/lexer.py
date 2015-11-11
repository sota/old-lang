
import os
from rpython.rtyper.lltypesystem import rffi, lltype
from rpython.translator.tool.cbuild import ExternalCompilationInfo

from sast.tokens import Token

#pylint: disable=invalid-name

CTOKEN = rffi.CStruct(
    'CToken',
    ('start', rffi.LONG),
    ('end', rffi.LONG),
    ('kind', rffi.LONG),
    ('line', rffi.LONG),
    ('pos', rffi.LONG),
    ('skip', rffi.LONG))

CTOKENP = rffi.CArrayPtr(CTOKEN)
CTOKENPP = rffi.CArrayPtr(CTOKENP)

def deref(obj):
    return obj[0]

def escape(old):
    new = ''
    for char in old:
        if char == '\n':
            new += '\\'
            new += 'n'
        else:
            new += char
    return new

lib_dir = os.path.join(os.getcwd(), 'root/lib')
lexer_dir = os.path.join(os.getcwd(), 'src/lexer')
lexer_eci = ExternalCompilationInfo(
    include_dirs=[lexer_dir],
    includes=['lexer.h'],
    library_dirs=[lib_dir],
    libraries=['lexer'],
    use_cpp_linker=True)

c_scan = rffi.llexternal( #pylint: disable=invalid-name
    'scan',
    [rffi.CONST_CCHARP, CTOKENPP],
    rffi.LONG,
    compilation_info=lexer_eci)

class LookaheadBeyondEndOfTokens(Exception):
    pass

class NeedTokensOrSource(Exception):
    pass

class Lexer(object):

    def __init__(self):
        self.source = None
        self.tokens = []
        self.index = 0
        self.kind2name = {
            261: 'sym',
            262: 'num',
            263: 'str',
            264: 'cmt',
        }
        for c in xrange(40, 127):
            self.kind2name[c] = chr(c)

    def scan(self, source):

        self.index = 0
        self.source = source
        del self.tokens[:]
        with lltype.scoped_alloc(CTOKENPP.TO, 1) as ctokenpp:
            csource = rffi.cast(rffi.CONST_CCHARP, rffi.str2charp(source))
            result = c_scan(csource, ctokenpp)
            for i in range(result):
                ctoken  = deref(ctokenpp)[i]
                start   = rffi.cast(lltype.Signed, ctoken.c_start)
                end     = rffi.cast(lltype.Signed, ctoken.c_end)
                kind    = rffi.cast(lltype.Signed, ctoken.c_kind)
                line    = rffi.cast(lltype.Signed, ctoken.c_line)
                pos     = rffi.cast(lltype.Signed, ctoken.c_pos)
                skip    = rffi.cast(lltype.Signed, ctoken.c_skip) != 0
                name    = self.kind2name.get(kind, None)
                assert start >= 0, "start not >= 0"
                assert end >= 0, "end not >= 0"
                value   = self.source[start:end]
                self.tokens.append(Token(name, value, kind, line, pos, skip))
        return self.tokens

    def lookahead(self, distance, expect=None, skips=False):
        index = self.index
        token = None
        while distance:
            if index < len(self.tokens):
                token = self.tokens[index]
            else:
                break
            if token:
                if skips or not token.skip:
                    distance -= 1
            index += 1
        distance = index - self.index
        return token, distance, (token.kind == expect) if token and expect else expect

    def lookahead1(self, expect=None):
        return self.lookahead(1, expect)

    def lookahead2(self, expect=None):
        return self.lookahead(2, expect)

    def consume(self, *expects):
        token, distance, _ = self.lookahead1()
        if not token:
            raise Exception
        if len(expects):
            for expect in expects:
                if expect == token.name:
                    self.index += distance
                    return token
            return None
        self.index += distance
        return token

