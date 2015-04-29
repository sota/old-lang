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

extern "C" struct SotaTokens scan(const char *source) {
    printf("parse\n");
    struct SotaTokens tokens;
    return tokens;
}
