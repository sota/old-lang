
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
    'SotaToken',
    ('ts', rffi.LONG),
    ('te', rffi.LONG),
    ('tt', rffi.LONG))
CSOTATOKENP = rffi.CArrayPtr(CSOTATOKEN)
CSOTATOKENPP = rffi.CArrayPtr(CSOTATOKENP)

c_scan = rffi.llexternal(
    'scan',
    [rffi.CONST_CCHARP, CSOTATOKENPP],
    rffi.LONG,
    compilation_info=lexer_eci)

def deref(obj):
    return obj[0]

def scan(source):

    tokens = []
    with lltype.scoped_alloc(CSOTATOKENPP.TO, 1) as csotatokenpp:
        csource = rffi.cast(rffi.CONST_CCHARP, rffi.str2charp(source))
        result = c_scan(csource, csotatokenpp)
        for i in range(result):
            ctoken = deref(csotatokenpp)[i]
            ts = rffi.cast(rffi.SIZE_T, ctoken.c_ts)
            te = rffi.cast(rffi.SIZE_T, ctoken.c_te)
            value = source[ts:te]
            tokens.append(SotaToken(value, ctoken.c_ts, ctoken.c_te, ctoken.c_tt))
    return tokens

