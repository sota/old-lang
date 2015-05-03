/*
vim: syntax=cpp
*/

#include "lexer.h"

#include <string>
#include <sstream>
#include <iostream>
#include <algorithm>
#include "tclap/CmdLine.h"
#include <stdio.h>

extern "C" int scan(const char *source, struct SotaToken **tokens) {
    printf("scan: source=\n%s", source);
    int count = 3;
    *tokens = (struct SotaToken *)malloc(count * sizeof(struct SotaToken));
    for (int i=0; i<count; ++i) {
        struct SotaToken *token = &(*tokens)[i];
        token->source = source;
        token->pos = i;
        token->len = i;
        token->type = i;
    }
 
    return count;
}
/*
extern "C" int foo(char *source) {
    printf("source:\n%s", source);
    return 0;
}

extern "C" int bar(const char *source) {
    printf("source:\n%s", source);
    return 0;
}
*/
