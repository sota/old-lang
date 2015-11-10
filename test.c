#include <stdio.h>

#include "test.h"

extern int test(struct Pair **pairs);

int main(int argc, char *argv[]) {
    printf("test\n");
    struct Pair *pairs = NULL;
    int result = test(&pairs);
    printf("result = %d\n", result);
    for (int i=0; i<result; ++i) {
        printf("hi\n");
        printf("Pair {name=%s, value=%s}\n", pairs[i].name, pairs[i].value);
        printf("ho\n");
    }
    printf("buh-bye\n");
    return 0;
}
