#include <stdio.h>

#include "test.h"

extern int test1(struct Pair **pairs);
extern int test2(struct Pair *pairs);

int main(int argc, char *argv[]) {
    struct Pair *pairs = NULL;
    int count = test1(&pairs);
    printf("count = %d\n", count);
    for (int i=0; i<count; ++i) {
        printf("Pair {name=%s, value=%s}\n", pairs[i].name, pairs[i].value);
    }
    return 0;
}
