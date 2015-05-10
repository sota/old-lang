
import os
from rpython.rtyper.lltypesystem import rffi, lltype
from rpython.translator.tool.cbuild import ExternalCompilationInfo

lexer_dir = os.path.join(os.getcwd(), 'src/lexer')
lexer_eci = ExternalCompilationInfo(
    include_dirs=[lexer_dir],
    includes=['lexer.h'],
    library_dirs=[lexer_dir],
    libraries=['lexer'],
    use_cpp_linker=True)

SOTATOKEN = rffi.CStruct(
    'SotaToken',
    ('ts', rffi.LONG),
    ('te', rffi.LONG),
    ('type', rffi.LONG))
SOTATOKENP = rffi.CArrayPtr(SOTATOKEN)
SOTATOKENPP = rffi.CArrayPtr(SOTATOKENP)

c_scan = rffi.llexternal(
    'scan',
    [rffi.CONST_CCHARP, SOTATOKENPP],
    rffi.LONG,
    compilation_info=lexer_eci)

def deref(obj):
    return obj[0]

def scan(source):

    with lltype.scoped_alloc(SOTATOKENPP.TO, 1) as sotatokenpp:
        sotacode = rffi.cast(rffi.CONST_CCHARP, rffi.str2charp(source))
        result = c_scan(sotacode, sotatokenpp)
        for i in range(result):
            token = deref(sotatokenpp)[i]
            ts = rffi.cast(rffi.SIZE_T, token.c_ts)
            te = rffi.cast(rffi.SIZE_T, token.c_te)
            print '{ts=%s, te=%s, type=%s value=\"%s\"}' % (ts, te, token.c_type, source[ts:te])

