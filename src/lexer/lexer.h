#ifndef __SOTA_LEXER__
#define __SOTA_LEXER__ = 1

#define VERSION "0.1"

#ifdef __cplusplus
extern "C" {
#endif

#include <stdio.h>

struct SotaToken {
    const char *source;
    long pos;
    long len;
    long type;
};

int scan(const char *source, struct SotaToken **tokens);
/*
int foo(char *source);
int bar(const char *source);
*/
#ifdef __cplusplus
}
#endif

#endif /*__SOTA_LEXER__*/
