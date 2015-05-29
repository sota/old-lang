/*
vim: syntax=ragel
*/

#include "lexer.h"
#include "helper.h"

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

#define T(t,i,v) {i,v},
static std::map<long, const char *> TokenMap = {
    ASCII
    TOKENS
};
#undef T

#define TOKEN(ti) tokenlist.push_back({ts-source, te-source, ti, lh.line(ts), lh.pos(ts)})
#define TRIMMED_TOKEN(ti, trim) tokenlist.push_back({ts-source+trim, te-source-trim, ti, lh.line(ts), lh.pos(ts)})

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
    syntax          = '"'|"'"|'.'|','|'('|')'|'['|']'|'{'|'}'|';';
    symbol          = (any - ('#'|whitespace|newline|syntax))+;

    counter         = (any | newline @{lh.add_newline(fpc);})*;

    commenter := |*
        ("##" (any - newline)* newline) & counter => {
            TOKEN(TokenType::Comment);
            fgoto body;
        };

        ('#' (any - '#')* '#') & counter => {
            TOKEN(TokenType::Comment);
            fgoto body;
        };
    *|;

    literal := |*
        ('"' (any - '"')* '"') & counter => {
            TOKEN(TokenType::Literal);
            fgoto body;
        };

        ("'" (any - "'")* "'") & counter => {
            TOKEN(TokenType::Literal);
            fgoto body;
        };
    *|;

    body := |*

        whitespace => {
        };

        ';'? ' '* newline & counter => {
            if (nesting == 0) {
                TOKEN(TokenType::EOS);
                fgoto denter;
            }
        };

        ';' => {
            TOKEN(TokenType::EOS);
        };

        '#' => {
            fhold;
            fgoto commenter;
        };

        '"' | "'" => {
            fhold;
            fgoto literal;
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

            switch (lh.is_dent(te-ts)) {
                case 1:
                    TOKEN(TokenType::Indent);
                    break;
                case -1:
                    TOKEN(TokenType::Dedent);
                    break;
                default:
                    printf("1 really?\n");
                    break;
            }
            fgoto body;
        };

        /./ => {
            fhold;
            switch (lh.is_dent(te-ts-1)) {
                case 1:
                    //ignored on purpose
                    //otherwise file starts with
                    //erroneous indent
                    break;
                case -1:
                    TOKEN(TokenType::Dedent);
                    break;
                default:
                    printf("2 really?\n");
                    break;
            }
            fgoto body;
        };
    *|;

    write data nofinal;
}%%

extern "C" const char * token_name(long ti) {
    return TokenMap[ti];
}

extern "C" long scan(const char *source, struct CSotaToken **tokens) {
    std::ios::sync_with_stdio(false);
    std::vector<const char *> newlines;
    std::vector<CSotaToken> tokenlist;
    size_t length = strlen(source);

    const char *p = source;
    const char *pe = source + length;
    const char *eof = pe;
    const char *ts = p;
    const char *te = p;
    int nesting = 0;

    LexerHelper lh(p-1); //pretend that there was a newline before the first char

    %% write init;
    %% write exec;

    if (cs == sota_error) {
        // Machine failed before finding a token.
        cerr << "PARSE ERROR" << endl;
        exit(1);
    }
    int dents = lh.dents();
    for (int dent=0; dent < dents; ++dent) {
        tokenlist.push_back({(long)length, (long)length, TokenType::Dedent, lh.line(pe), lh.pos(pe)});
    }

    *tokens = (struct CSotaToken *)malloc(tokenlist.size() * sizeof(struct CSotaToken));
    copy(tokenlist.begin(), tokenlist.end(), *tokens);
    return tokenlist.size();
}

