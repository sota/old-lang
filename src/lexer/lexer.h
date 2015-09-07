#ifndef __LEXER__
#define __LEXER__ = 1

#ifdef __cplusplus
extern "C" {
#endif

#include "token.h"

long scan(const char *source, struct CToken **tokens);

#ifdef __cplusplus
}
#endif

#endif /*__LEXER__*/
