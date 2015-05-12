/*
vim: syntax=cpp
*/

#include "lexer.h"

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

static int cs;
static int act;
static int spaces = 0;
static int dentsize = 0;
static int parenthesis = 0;
static const char *ts = NULL;
static const char *te = NULL;

#define T(t,i,v) {t,v},
static std::map<enum TokenType, const char *> TokenMap = {
    TOKENS
};
#undef T

#define TOKEN(ti) tokenlist.push_back({ts-source, te-source, ti})
#define TRIMMED_TOKEN(ti, trim) tokenlist.push_back({ts-source+trim, te-source-trim, ti})

%%{
    machine sota;
    write data nofinal;

    action eponymous_tok {
        char c = *ts;
        if (c == '(')
            ++parenthesis;
        else if (c == ')')
            --parenthesis;
        TOKEN((long)*ts);
    }

    action denter_tok {
        int count = 0;
        const char *s = ts;
        while (s != te) {
            switch (*s) {
                case '\n':
                case '\r':
                    count = 0;
                    break;
                default:
                    ++count;
                    break;
            }
            ++s;
        }
        if (dentsize == 0)
            dentsize = count;
        if (count != spaces) {
            if (count == spaces + dentsize)
                TOKEN(TokenType::Indent);
            else if (count == spaces - dentsize)
                TOKEN(TokenType::Dedent);
            else {
                printf("DENTING ERROR!\n");
            }
        }
        else if (parenthesis)
            TOKEN(',');
        else
            TOKEN(';');
        spaces = count;
    }

    action number_tok {
        TOKEN(TokenType::Number);
    }

    action symbol_tok {
        TOKEN(TokenType::Symbol);
    }

    action literal_tok {
        TRIMMED_TOKEN(TokenType::Literal, 1);
    }

    action comment_tok {
        TOKEN(TokenType::Comment);
    }

    whitespace      = ' '+;
    newline         = "\n\r"|'\n'|'\r';
    denter          = (newline ' '*)+;
    reserved        = '='|'('|')'|'['|']'|'{'|'}'|'.'|','|':'|';';
    symbol          = (any - (reserved|space))*;
    number          = [0-9]+('.'[0-9]+)?;
    literal         = "\"" any* :>> "\"";
    comment         = "##" (any* - '#') :>> "##" | '#'+ any* :>> newline;

    scan := |*
        reserved        => eponymous_tok;
        symbol          => symbol_tok;
        number          => number_tok;
        literal         => literal_tok;
        comment         => comment_tok;
        denter          => denter_tok;
        whitespace;
    *|;

}%%

extern "C" long scan(const char *source, struct CSotaToken **tokens) {

    std::vector<CSotaToken> tokenlist;
    size_t length = strlen(source);
    const char *p = source;
    const char *pe = source + length;
    const char *eof = pe;

    %% write init;
    %% write exec;

    *tokens = (struct CSotaToken *)malloc(tokenlist.size() * sizeof(struct CSotaToken));
    copy(tokenlist.begin(), tokenlist.end(), *tokens);
    return tokenlist.size();
}
