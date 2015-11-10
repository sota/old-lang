#include "test.h"

#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include <vector>

extern "C" int test(struct Pair **pairs) {
    srand(time(NULL));
    int count = rand() % 10;
    printf("count = %d", count);
    return count;
}
