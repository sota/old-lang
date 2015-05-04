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
#include <string.h>

#define SOTA_Number         258
#define SOTA_Symbol         259
#define SOTA_RightArrow     261
#define SOTA_PlusPlus       262
#define SOTA_MinusMinus     263
#define SOTA_EqualsEquals   271
#define SOTA_NotEquals      272
#define SOTA_AndAnd         273
#define SOTA_OrOr           274
#define SOTA_AddAssign      275
#define SOTA_SubAssign      276
#define SOTA_MulAssign      277
#define SOTA_DivAssign      278
#define SOTA_ModAssign      279
#define SOTA_DotDot         280
#define SOTA_DotDotDot      281
#define SOTA_Whitespace     282
#define SOTA_Comment        283


using std::cerr;
using std::cout;
using std::cin;
using std::endl;

static int cs;
static int act;
static const char *ts;
static const char *te;

%%{
    machine sota;

    action num_tok {
        struct SotaToken token = {
            0,
            1,
            SOTA_Number,
        };
        tokenlist.push_back(token);
    }

    action add_tok {
        struct SotaToken token = {
            0,
            1,
            '+',
        };
        tokenlist.push_back(token);
    }

    action sub_tok {
        struct SotaToken token = {
            0,
            1,
            '-',
        };
        tokenlist.push_back(token);
    }

    action mul_tok {
        struct SotaToken token = {
            0,
            1,
            '*',
        };
        tokenlist.push_back(token);
    }

    action div_tok {
        struct SotaToken token = {
            0,
            1,
            '/',
        };
        tokenlist.push_back(token);
    }

    action op_tok {
        struct SotaToken token = {
            0,
            1,
            '(',
        };
        tokenlist.push_back(token);
    }

    action cp_tok {
        struct SotaToken token = {
            0,
            1,
            ')',
        };
        tokenlist.push_back(token);
    }

    action semi_tok {
        struct SotaToken token = {
            0,
            1,
            ';',
        };
        tokenlist.push_back(token);
    }

    num = [0-9]+('.'[0-9]+)?;
    add = '+';
    sub = '-';
    mul = '*';
    div = '/';
    op = '(';
    cp = ')';
    semi = ';';

    scan := |*
        num => num_tok;
        add => add_tok;
        sub => sub_tok;
        mul => mul_tok;
        div => div_tok;
        op => op_tok;
        cp => cp_tok;
        semi => semi_tok;
        space;
    *|;

}%%

%% write data;

extern "C" long scan(const char *source, struct SotaToken **tokens) {
    std::vector<SotaToken> tokenlist;

    size_t length = strlen(source);
    const char *p = source;
    const char *pe = source + length;
    const char *eof = pe;

    %% write init;
    %% write exec;

    *tokens = &tokenlist[0];
    printf("tokenlist.size()=%ld\n", tokenlist.size());
    return tokenlist.size();
}
