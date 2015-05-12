#ifndef __SOTA_LEXER__
#define __SOTA_LEXER__ = 1

#ifdef __cplusplus
extern "C" {
#endif

#include <stdio.h>
#include <string.h>

#include "token.h"

long scan(const char *source, struct CSotaToken **tokens);

#ifdef __cplusplus
}
#endif

#endif /*__SOTA_LEXER__*/
