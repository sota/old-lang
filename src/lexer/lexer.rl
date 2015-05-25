/*
vim: syntax=ragel
*/

#include "lexer.h"

#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include <map>
#include <string>
#include <sstream>
#include <iostream>
#include <algorithm>
#include "tclap/CmdLine.h"

using std::cerr;
using std::cout;
using std::cin;
using std::endl;
using std::copy;

#define T(t,i,v) {t,v},
static std::map<enum TokenType, const char *> TokenMap = {
    TOKENS
};
#undef T

#define TOKEN(ti) tokenlist.push_back({ts-source, te-source, ti, line, ts-ls+1})
#define TRIMMED_TOKEN(ti, trim) tokenlist.push_back({ts-source+trim, te-source-trim, ti, line, ts-ls+1})

static int cs, act;
int stack[1], top;

inline void write(const char *data) {
    cout << data;
}

inline void write(const char c) {
    cout << c;
}

inline void write(const char *data, int len) {
    cout.write(data, len);
}

%%{
    machine sota;

    whitespace      = ' '+;
    newline         = "\n\r"|'\n'|'\r';
    number          = digit+ ('.' digit+)?;
    syntax          = '.'|','|'('|')'|'['|']'|'{'|'}'|';';
    symbol          = (any - ('#'|whitespace|newline|syntax))+;

    commentline := |*
        "##" (any - newline)* => {
            TOKEN(TokenType::Comment);
        };

        newline => {
            if (nesting == 0) {
                TOKEN(TokenType::Newline);
                ++line;
                ls = te;
                fgoto denter;
            }
        }
    *|;

    comment := |*
        '#' (any - '#')* '#' => {
            TOKEN(TokenType::Comment);
            fgoto body;
        };
    *|;

    body := |*

        whitespace => {
        };

        newline => newline_action;

        "##" => {
            fhold;
            fhold;
            fgoto commentline;
        };

        '#' => {
            fhold;
            fgoto comment;
        };

        '\t' => {
            printf("TAB ERROR\n");
            exit(-1);
        };

        '{'|'['|'(' => {
            TOKEN(fc);
            ++nesting;
            if ('{' == fc)
                fcall body;
        };

        '}'|']'|')' => {
            TOKEN(fc);
            --nesting;
            if ('}' == fc)
                fret;
        };

        number => {
            TOKEN(TokenType::Number);
        };

        symbol => {
            TOKEN(TokenType::Symbol);
        };

        syntax => {
            TOKEN(fc);
        };


    *|;

    denter := |*
        whitespace* => {
            int spaces = te-ts;
            if (dentsize == 0)
                dentsize = spaces;
            if (spaces == indents + dentsize)
                TOKEN(TokenType::Indent);
            else if (spaces == indents - dentsize)
                TOKEN(TokenType::Dedent);
            else if (spaces == indents)
                TOKEN(TokenType::Newline);
            else
                printf("DENTING ERROR: spaces=%d indents=%d dentsize=%d\n", spaces, indents, dentsize);
            indents = spaces;
            fgoto body;
        };

        /./ => {
            fhold;
            int spaces = te-ts-1;
            if (dentsize && (spaces == indents - dentsize))
                TOKEN(TokenType::Dedent);
            fgoto body;
        };
    *|;

    write data nofinal;
}%%

extern "C" long scan(const char *source, struct CSotaToken **tokens)
{
    std::ios::sync_with_stdio(false);
    std::vector<const char *> newlines;
    std::vector<CSotaToken> tokenlist;
    size_t length = strlen(source);

    const char *p = source;
    const char *pe = source + length;
    const char *eof = pe;
    const char *ts = p;
    const char *te = p;
    const char *ls = p;
    long line = 1;
    int indents = 0;
    int dentsize = 0;
    int nesting = 0;

    %% write init;
    %% write exec;

    if (cs == sota_error) {
        // Machine failed before finding a token.
        cerr << "PARSE ERROR" << endl;
        exit(1);
    }

    *tokens = (struct CSotaToken *)malloc(tokenlist.size() * sizeof(struct CSotaToken));
    copy(tokenlist.begin(), tokenlist.end(), *tokens);
    return tokenlist.size();
}

