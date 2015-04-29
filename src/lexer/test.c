#include <stdio.h>

#include "lexer.h"

extern int parse(int argc, char *argv[], struct SotaToken **tokens);

int main(int argc, char *argv[]) {
    printf("test\n");
    struct SotaToken *tokens = NULL;
    int result = scan("source", &tokens);
    printf("result = %d\n", result);
    for (int i=0; i<result; ++i) {
        printf("SotaToken {name=%s, value=%s, line=%ld, pos=%ld}\n", tokens[i].name, tokens[i].value, tokens[i].line, tokens[i].pos);
    }
    printf("buh-bye\n");
    return 0;
}
