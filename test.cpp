#include "test.h"

#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include <vector>

std::vector<struct Pair> gen_pairs() {
    srand(time(NULL));
    std::vector<struct Pair> pairlist;

    char const *foo = "foo";
    char const *bar = "bar";
    int count = rand() % 5 + 1;
    for (int i=0; i<count; ++i) {
        pairlist.push_back({
            .name = (char *)foo,
            .value = (char *)bar
        });
    }
    return pairlist;
}

extern "C" int test1(struct Pair **pairs) {
    std::vector<struct Pair> pairlist = gen_pairs();
    *pairs = (struct Pair *)malloc(pairlist.size() * sizeof(struct Pair));
    copy(pairlist.begin(), pairlist.end(), *pairs);
    return pairlist.size();
}

extern "C" int test2(struct Pair *pairs) {
    std::vector<struct Pair> pairlist = gen_pairs();
    pairs = (struct Pair *)malloc(pairlist.size() * sizeof(struct Pair));
    copy(pairlist.begin(), pairlist.end(), pairs);
    return pairlist.size();
}
