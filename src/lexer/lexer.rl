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
static const char *ts = NULL;
static const char *te = NULL;

#define T(t,i,v) {t,v},
static std::map<enum TokenType,const char *> TokenMap = {
    TOKENS
};
#undef T

#define TOKEN(i) tokenlist.push_back({ts-source, te-source, i})

%%{
    machine sota;
    write data nofinal;

    action assign_tok {
        TOKEN('=');
    }

    action comma_tok {
        TOKEN(',');
    }

    action openparen_tok {
        TOKEN('(');
    }

    action closeparen_tok {
        TOKEN(')');
    }

    action semicolon_tok {
        TOKEN(';');
    }

    action number_tok {
        TOKEN(TokenType::Number);
    }

    action symbol_tok {
        TOKEN(TokenType::Symbol);
    }

    action rightarrow_tok {
        TOKEN(TokenType::RightArrow);
    }

    action literal_tok {
        TOKEN(TokenType::Literal);
    }

    action comment_tok {
        TOKEN(TokenType::Comment);
    }

    assign      = '=';
    comma       = ',';
    openparen   ='(';
    closeparen  = ')';
    semicolon   = ';';
    number      = [0-9]+('.'[0-9]+)?;
    op          = [+\-*\/:=^&%$@!~<>]+;
    alpha_      = (alpha | '_');
    alnum_      = (alnum | '_');
    syms        = '_' | '-' | '+' | '&';
    id          = (digit+ (alpha | syms) | alpha | '_') (syms? (alnum | '_' | '?'))*;
    symbol      = op | id;
    rightarrow  = "->";
    literal     = "\"" any* :>> "\"";
    comment     = "##" any* :>> "##" | '#' [^\n\r]+;

    scan := |*
        assign      => assign_tok;
        comma       => comma_tok;
        openparen   => openparen_tok;
        closeparen  => closeparen_tok;
        semicolon   => semicolon_tok;
        rightarrow  => rightarrow_tok;
        number      => number_tok;
        symbol      => symbol_tok;
        literal     => literal_tok;
        comment     => comment_tok;
        space;
    *|;

}%%

extern "C" const char * token_value(int tokenType) {
    if (0 <= tokenType && tokenType <= 255) {
        std::string s;
        s.insert(0, 1, (char)tokenType);
        return s.c_str();
    }
    else if (TokenMap.find((enum TokenType)tokenType) != TokenMap.end()) {
        return TokenMap[(enum TokenType)tokenType];
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
