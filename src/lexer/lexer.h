#ifndef __SOTA_LEXER__
#define __SOTA_LEXER__ = 1

typedef struct {
    const char *name;
    const char *value;
    const int line;
    const int pos;
} SotaToken;

void foo();
int scan(const char *filename, SotaToken *tokens);

#endif /*__SOTA_LEXER__*/
