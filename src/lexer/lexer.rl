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
    printf("parse\n");
    int count = 3;
    *tokens = (struct SotaToken *)malloc(count * sizeof(struct SotaToken));
    for (int i=0; i<count; ++i) {
        struct SotaToken *token = &(*tokens)[i];
        token->name = "si";
        token->value = "og";
        token->line = i;
        token->pos = i;
    }
 
    return count;
}
