#include <stdio.h>

#include "cli.h"

extern int parse(int argc, char *argv[], struct CliToken **tokens);

int main(int argc, char *argv[]) {
    printf("test\n");
    struct CliToken *tokens = NULL;
    int result = parse(argc, argv, &tokens);
    printf("result = %d\n", result);
    for (int i=0; i<result; ++i) {
        printf("CliToken {name=%s, value=%s}\n", tokens[i].name, tokens[i].value);
    }
    printf("buh-bye\n");
    return 0;
}
