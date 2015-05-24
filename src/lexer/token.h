#ifndef __SOTA_TOKEN__
#define __SOTA_TOKEN__ = 1

#ifdef __cplusplus
extern "C" {
#endif

#define TOKENS                          \
T(Newline,      258,    "<NEWLINE>")    \
T(Indent,       259,    "<INDENT>")     \
T(Dedent,       260,    "<DEDENT>")     \
T(Symbol,       261,    "<SYMBOL>")     \
T(Number,       262,    "<NUMBER>")     \
T(Literal,      263,    "<LITERAL>")    \
T(Comment,      264,    "<COMMENT>")    \
T(Lambda,       265,    "->")           \

#define T(t,i,v) t=i,
enum TokenType {
    TOKENS
};
#undef T

//static std::map<TokenType, std::string> TokenMap;

struct CSotaToken {
    long ts;    //token start
    long te;    //token end
    long ti;    //token id
    long line;  //token line
    long pos;   //token pos
};

#ifdef __cplusplus
}
#endif

#endif /*__SOTA_TOKEN__*/
