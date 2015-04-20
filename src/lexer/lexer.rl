/*
vim: syntax=c
*/

#include "lexer.h"

long foo(Point *point) {
    printf("foo\n");
    if (point) {
        printf("{x=%ld,y=%ld}\n", point->x, point->y);
    }
    else {
        printf("pre malloc\n");
        point = (Point *)malloc(sizeof(Point));
        printf("post malloc\n");
        point->x = 1;
        point->y = 2;
        printf("point->x=%ld point->y=%ld\n", point->x, point->y);
    }
    return 0;
}

long scan(const char *source, SotaToken *tokens) {
    printf("scan: source=%s", source);
    return 0;
}
