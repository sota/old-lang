#include <stdio.h>

#include "lexer.h"

extern long scan(const char *source, struct SotaToken **tokens);

int main(int argc, char *argv[]) {
    printf("test\n");
    struct SotaToken *tokens = NULL;
    long result = scan("1+2;", &tokens);
    printf("result = %ld\n", result);
    for (int i=0; i<result; ++i) {
        printf("SotaToken {index=%lu, length=%lu, type=%lu}\n", tokens[i].index, tokens[i].length, tokens[i].type);
    }
    printf("buh-bye\n");
    return 0;
}
