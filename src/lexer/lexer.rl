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
static std::map<enum TokenType,const char *> TokenMap = {
    TOKENS
};
#undef T

#define TOKEN(tt) tokenlist.push_back({ts-source, te-source, tt})
#define TRIMMED_TOKEN(tt, trim) tokenlist.push_back({ts-source+trim, te-source-trim, tt})

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
        int count = (te - ts) - 1;
        if (dentsize == 0)
            dentsize = count;
        if (count != spaces) {
            if (count == spaces + dentsize)
                TOKEN(TokenType::Indent);
            else if (count == spaces - dentsize)
                TOKEN(TokenType::Dedent);
            else {
                printf("DENTING ERROR!\n");
                int position = ts-source;
                int length = te-ts;
                printf("position=%d length=%d count=%d spaces=%d\n", position, length, count, spaces);
            }
        }
        else if (parenthesis)
            TOKEN(TokenType::EOE);
        else
            TOKEN(TokenType::EOS);
        spaces = count;
    }

    action number_tok {
        TOKEN(TokenType::Number);
    }

    action symbol_tok {
        TOKEN(TokenType::Symbol);
    }

    action lambda_tok {
        TOKEN(TokenType::Lambda);
    }

    action literal_tok {
        TRIMMED_TOKEN(TokenType::Literal, 1);
    }

    action comment_tok {
        TOKEN(TokenType::Comment);
    }

    whitespace      = ' '+;
    newline         = "\n\r"|'\n'|'\r';
    denter          = newline ' '*;
    reserved        = '='|'('|')'|'['|']'|'{'|'}'|'.'|','|':'|';';
    symbol          = (any - (reserved|space))*;
    number          = [0-9]+('.'[0-9]+)?;
    lambda          = "->";
    literal         = "\"" any* :>> "\"";
    comment         = "##" (any* - '#') :>> "##" | '#'+ any* :>> newline;

    scan := |*
        reserved        => eponymous_tok;
        symbol          => symbol_tok;
        number          => number_tok;
        lambda          => lambda_tok;
        literal         => literal_tok;
        comment         => comment_tok;
        denter          => denter_tok;
        whitespace;
    *|;

}%%

extern "C" const char * token_value(int tt) {
    if (0 <= tt && tt <= 255) {
        std::string s;
        s.insert(0, 1, (char)tt);
        return s.c_str();
    }
    else if (TokenMap.find((enum TokenType)tt) != TokenMap.end()) {
        return TokenMap[(enum TokenType)tt];
    }
    else {
        printf("token_value: error!\n");
        return NULL;
    }
}

extern "C" long scan(const char *source, struct SotaToken **tokens) {

    std::vector<SotaToken> tokenlist;
    size_t length = strlen(source);
    const char *p = source;
    const char *pe = source + length;
    const char *eof = pe;

    %% write init;
    %% write exec;

    *tokens = (struct SotaToken *)malloc(tokenlist.size() * sizeof(struct SotaToken));
    copy(tokenlist.begin(), tokenlist.end(), *tokens);
    return tokenlist.size();
}
