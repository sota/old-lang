#include <stdio.h>

#include "lexer.h"

extern const char * token_value(int tokeType);
extern long scan(const char *source, struct CToken **tokens);

int main(int argc, char *argv[]) {
    printf("test\n");
    struct CToken *tokens = NULL;
    long result = scan("1+2;", &tokens);
    printf("result = %ld\n", result);
    for (int i=0; i<result; ++i) {
        printf("Token {start=%ld, end=%ld, kind=%ld, line=%ld, pos=%ld}\n", tokens[i].start, tokens[i].end, tokens[i].kind, tokens[i].line, tokens[i].pos);
    }
    printf("buh-bye\n");
    return 0;
}
