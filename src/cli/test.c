#include <stdio.h>
#include <assert.h>

#include "cli.h"

extern CliTokens * parse(int argc, char *argv[]);

int main(int argc, char *argv[]) {
    printf("test\n");
    struct CliTokens *tokens = parse(argc, argv);
    for (int i=0; i<tokens->count; ++i) {
        printf("CliToken {name=%s, value=%s}\n", tokens->tokens[i].name, tokens->tokens[i].value);
    }
    int result = clean(tokens);
    assert(result == 0);
    printf("buh-bye\n");
    return 0;
}
