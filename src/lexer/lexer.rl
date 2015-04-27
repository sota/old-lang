/*
vim: syntax=c
*/

#include "lexer.h"

size_t foo(struct Point *ppoints[]) {
    size_t count = 5;
    struct Point *points = malloc(count * sizeof(struct Point));
    for (size_t i=0; i<count; ++i) {
        points[i].x = points[i].y = i;
    }
    *ppoints = points;
    return count;
}

long scan(const char *source, SotaToken *tokens) {
    printf("scan: source=%s", source);
    return 0;
}
