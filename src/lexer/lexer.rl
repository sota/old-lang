/*
vim: syntax=c
*/

#include <stdio.h>

#include "lexer.h"

void foo() {
    printf("c version\n");
}

int scan(const char *filename, SotaToken *tokens) {
    printf("scan: filename=%s", filename);
    return 0;
}
