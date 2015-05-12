#include <stdio.h>

#include "lexer.h"

extern const char * token_value(int tokeType);
extern long scan(const char *source, struct CSotaToken **tokens);

int main(int argc, char *argv[]) {
    printf("test\n");
    struct CSotaToken *tokens = NULL;
    long result = scan("1+2;", &tokens);
    printf("result = %ld\n", result);
    for (int i=0; i<result; ++i) {
        printf("SotaToken {ts=%ld, te=%ld, ti=%ld}\n", tokens[i].ts, tokens[i].te, tokens[i].ti);
    }
    printf("buh-bye\n");
    return 0;
}
