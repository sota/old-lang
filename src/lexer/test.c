#include <stdio.h>

#include "lexer.h"

extern struct CliTokens parse(int argc, char *argv[]);

int main(int argc, char *argv[]) {
    printf("test\n");
    struct SotaTokens tokens = scan("source");
    printf("%p\n", &tokens);
    printf("buh-bye\n");
    return 0;
}
