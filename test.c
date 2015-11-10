#include <stdio.h>

#include "test.h"

extern int test(struct Pair **pairs);

int main(int argc, char *argv[]) {
    printf("test\n");
    struct Pair *pair = NULL;
    int result = test(&tokens);
    printf("result = %d\n", result);
    for (int i=0; i<result; ++i) {
        printf("Pair {name=%s, value=%s}\n", pairs[i].name, pairs[i].value);
    }
    printf("buh-bye\n");
    return 0;
}
