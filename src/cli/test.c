#include <stdio.h>

#include "cli.h"

extern struct CliTokens parse(int argc, char *argv[]);

int main(int argc, char *argv[]) {
    printf("test\n");
    struct CliTokens tokens = parse(argc, argv);
    printf("%p\n", &tokens);
    printf("buh-bye\n");
    return 0;
}
