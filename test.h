#ifndef __TEST__
#define __TEST__ = 1

#ifdef __cplusplus
extern "C" {
#endif

struct Pair {
    char *name;
    char *value;
};

int test1(struct Pair **pairs);
int test2(struct Pair *pairs);

#ifdef __cplusplus
}
#endif

#endif /*__TEST__*/
