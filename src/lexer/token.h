#ifndef __TOKEN__
#define __TOKEN__ = 1

#ifdef __cplusplus
extern "C" {
#endif

#define TOKENS                          \
T(EndOfFile,    EOF,    "<EOF>")        \
T(StartOfFile,  260,    "<SOF>")        \
T(Symbol,       261,    "<SYMBOL>")     \
T(Number,       262,    "<NUMBER>")     \
T(String,       263,    "<STRING>")     \
T(Comment,      264,    "<COMMENT>")    \

#define T(t,i,v) t=i,
enum TokenKind {
    TOKENS
};
#undef T

struct CToken {
    long start;
    long end;
    long kind;
    long line;
    long pos;
    long skip;
};

#ifdef __cplusplus
}
#endif

#endif /*__TOKEN__*/
