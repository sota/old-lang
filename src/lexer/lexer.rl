/*
vim: syntax=ragel
*/

#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include <map>
#include <string>
#include <vector>
#include <sstream>
#include <iostream>
#include <algorithm>
#include <exception>
#include <stdexcept>

#include "lexer.h"
#include "ascii.h"

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
    machine sast;

    whitespace      = ' '+;
    tab             = '\t';
    hash            = '#';
    doublequote     = '"';
    newline         = "\n\r"|'\n'|'\r';
    number          = digit+ ('.' digit+)?;
    syntax          = '"'|"'"|'.'|'('|')'|'['|']'|'{'|'}'|';';
    symbol          = (any - ('#'|whitespace|newline|syntax))+;
    counter         = (any | newline @{AddNewline(fpc);})*;

    commenter := |*
        ("##" (any - newline)* newline) & counter => {
            Token(TokenKind::Comment);
            fgoto body;
        };

        ('#' (any - '#')* '#') & counter => {
            Token(TokenKind::Comment);
            fgoto body;
        };
    *|;

    string := |*
        ('"' (any - '"')* '"') & counter => {
            Token(TokenKind::String, 1);
            fgoto body;
        };
    *|;

    body := |*

        whitespace => {
        };

        ' '* newline & counter => {
        };

        hash => {
            fhold;
            fgoto commenter;
        };

        doublequote => {
            fhold;
            fgoto string;
        };

        tab => {
            printf("TAB ERROR\n");
            exit(-1);
        };

        '{'|'['|'(' => {
            Token(fc);
            ++nesting;
        };

        '}'|']'|')' => {
            Token(fc);
            --nesting;
        };

        number => {
            Token(TokenKind::Number);
        };

        "'" => {
            Token(TokenKind::Symbol);
        };

        symbol => {
            Token(TokenKind::Symbol);
        };

        syntax => {
            Token(fc);
        };

    *|;

    write data nofinal;
}%%

class Lexer {
    char const* const source;
    char const* const pe;
    char const* const eof;
    char const* p;
    char const* ts;
    char const* te;
    int stack[1];
    int cs;
    int act;
    int top;
    int nesting;
    std::vector<const char *> newlines;
    std::vector<CToken> tokens;

public:
    Lexer(char const* const source)
        : source(source)
        , pe(source + strlen(source))
        , eof(source + strlen(source))
        , p(source)
        , nesting(0) {
        %% write init;
        //pretend newline before start of file
        newlines.push_back(source-1);
    }

    ~Lexer() {
        newlines.clear();
        tokens.clear();
    }

    void AddNewline(const char *pchar) {
        if (pchar > newlines.back())
            newlines.push_back(pchar);
        else
            printf("UNEXPECTED BEHAVIOR!!!\n");
    }

    const char * Newline(const char *pchar) {
        for (unsigned i = newlines.size(); i-- > 0;) {
            if (pchar > newlines[i])
                return newlines[i];
        }
        return 0;
    }

    long Line(const char *pchar) {
        for (unsigned i = newlines.size(); i-- > 0;) {
            if (pchar > newlines[i])
                return i + 1;
        }
        return 0;
    }

    long Pos(const char *pchar) {
        const char *nl = Newline(pchar);
        if (nl)
            return pchar - nl;
        return 0;
    }

    void Token(long kind, long trim=0) {
        tokens.push_back({
            ts - source + trim,
            te - source - trim,
            kind,
            Line(ts),
            Pos(ts)});
    }

    void Token(long start, long end, long kind, long line, long pos, long skip) {
        tokens.push_back({
            start,
            end,
            kind,
            line,
            pos,
            skip});
    }

    long Scan(CToken **tokens) {
        Token(0, 0, '{', 0, 0, 0);
        %% write exec;
        Token(0, 0, '}', eof - p, eof - p, 0);
        *tokens = (struct CToken *)malloc(this->tokens.size() * sizeof(struct CToken));
        copy(this->tokens.begin(), this->tokens.end(), *tokens);
        return this->tokens.size();
    }

};

extern "C" long scan(const char *source, struct CToken **tokens) {
    std::ios::sync_with_stdio(false);
    Lexer lexer(source);
    return lexer.Scan(tokens);
}

