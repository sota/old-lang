#ifndef __SOTA_LEXER__
#define __SOTA_LEXER__ = 1

#define VERSION "0.1"

#ifdef __cplusplus
extern "C" {
#endif

#include <stdio.h>

struct SotaToken {
    size_t index;
    size_t length;
    size_t type;
};

long scan(const char *source, struct SotaToken **tokens);

#ifdef __cplusplus
}
#endif

#endif /*__SOTA_LEXER__*/
