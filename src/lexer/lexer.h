#ifndef __SOTA_LEXER__
#define __SOTA_LEXER__ = 1

#include <stdio.h>
#include <stdlib.h>

typedef struct {
    const char *name;
    const char *value;
    const long line;
    const long pos;
} SotaToken;

/*
typedef struct {
    long x;
    long y;
} Point;

long foo(Point **points);
*/
struct Point {
    long x;
    long y;
};
size_t foo(struct Point *ppoints[]);
long scan(const char *source, SotaToken *tokens);

#endif /*__SOTA_LEXER__*/
