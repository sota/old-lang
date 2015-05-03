#include <stdio.h>

#include "lexer.h"

extern int parse(int argc, char *argv[], struct SotaToken **tokens);

int main(int argc, char *argv[]) {
    printf("test\n");
    struct SotaToken *tokens = NULL;
    int result = scan("source", &tokens);
    printf("result = %d\n", result);
    for (int i=0; i<result; ++i) {
        printf("SotaToken {source=%s, pos=%ld, len=%ld, type=%ld}\n", tokens[i].source, tokens[i].pos, tokens[i].len, tokens[i].type);
    }
    printf("buh-bye\n");
    return 0;
}
