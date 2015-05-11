#ifndef __SOTA_TOKEN__
#define __SOTA_TOKEN__ = 1

#ifdef __cplusplus
extern "C" {
#endif

#define TOKENS                          \
T(EOS,          257,    "<EOS>")        \
T(EOE,          258,    "<EOE>")        \
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

struct SotaToken {
    long ts;    //token start
    long te;    //token end
    long tt;    //token type
};

#ifdef __cplusplus
}
#endif

#endif /*__SOTA_TOKEN__*/
