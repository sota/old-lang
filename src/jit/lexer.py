
import os
from rpython.rtyper.lltypesystem import rffi, lltype
from rpython.translator.tool.cbuild import ExternalCompilationInfo

from tokens import SotaToken

lexer_dir = os.path.join(os.getcwd(), 'src/lexer')
lexer_eci = ExternalCompilationInfo(
    include_dirs=[lexer_dir],
    includes=['lexer.h'],
    library_dirs=[lexer_dir],
    libraries=['lexer'],
    use_cpp_linker=True)

CSOTATOKEN = rffi.CStruct(
    'CSotaToken',
    ('ts', rffi.LONG),
    ('te', rffi.LONG),
    ('ti', rffi.LONG),
    ('line', rffi.LONG),
    ('pos', rffi.LONG))
CSOTATOKENP = rffi.CArrayPtr(CSOTATOKEN)
CSOTATOKENPP = rffi.CArrayPtr(CSOTATOKENP)

c_scan = rffi.llexternal(
    'scan',
    [rffi.CONST_CCHARP, CSOTATOKENPP],
    rffi.LONG,
    compilation_info=lexer_eci)

def deref(obj):
    return obj[0]

def escape(old):
    new = ''
    for c in old:
        if c == '\n':
            new += '\\'
            new += 'n'
        else:
            new += c
    return new

def scan(source):

    tokens = []
    with lltype.scoped_alloc(CSOTATOKENPP.TO, 1) as csotatokenpp:
        csource = rffi.cast(rffi.CONST_CCHARP, rffi.str2charp(source))
        result = c_scan(csource, csotatokenpp)
        for i in range(result):
            ctoken = deref(csotatokenpp)[i]
            ts = rffi.cast(rffi.SIZE_T, ctoken.c_ts)
            te = rffi.cast(rffi.SIZE_T, ctoken.c_te)
            value = escape(source[ts:te])
            if ctoken.c_ti == 257:
                name = 'EOS'
            elif ctoken.c_ti == 258:
                name = 'EOE'
            elif ctoken.c_ti == 259:
                name = 'INDENT'
            elif ctoken.c_ti == 260:
                name = 'DEDENT'
            elif ctoken.c_ti == 261:
                name = 'SYM'
            elif ctoken.c_ti == 262:
                name = 'NUM'
            elif ctoken.c_ti == 263:
                name = 'LIT'
            elif ctoken.c_ti == 264:
                name = 'CMT'
            elif ctoken.c_ti == 265:
                name = '->'
            else:
                name = value
            tokens.append(SotaToken(name, value, ctoken.c_line, ctoken.c_pos))
    return tokens

