#ifndef __SOTA_LEXER__
#define __SOTA_LEXER__ = 1

#define VERSION "0.1"

#ifdef __cplusplus
extern "C" {
#endif

#include <stdio.h>
#include <string.h>
/*
#define SOTA_Symbol         256
#define SOTA_Number         257
#define SOTA_Match          258
#define SOTA_Search         259
#define SOTA_Replace        260
#define SOTA_RightArrow     261
*/
#define TOKENS                          \
T(RightArrow,   256,    "->")           \
T(Indent,       257,    "<INDENT>")     \
T(Dedent,       258,    "<DEDENT>")     \
T(Symbol,       259,    "<SYM>")        \
T(Number,       260,    "<NUM>")        \
T(Literal,      261,    "<LIT>")        \
T(Comment,      262,    "<COMMENT>")    \
T(True,         263,    "true")         \
T(False,        264,    "false")        \
T(Skip,         265,    "skip")         \
T(Null,         266,    "null")         \
T(Match,        267,    "match")        \
T(Search,       268,    "s/")           \
T(Replace,      269,    "r/")           \

#define T(t,i,v) t=i,
enum TokenType {
    TOKENS
};
#undef T

//static std::map<TokenType, std::string> TokenMap;

struct SotaToken {
    long ts;    //token start
    long te;    //token end
    long tt;    //token type
};


const char * token_value(int tt);
long scan(const char *source, struct SotaToken **tokens);

#ifdef __cplusplus
}
#endif

#endif /*__SOTA_LEXER__*/
