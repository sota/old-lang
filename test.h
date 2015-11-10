#ifndef __TEST__
#define __TEST__ = 1

#ifdef __cplusplus
extern "C" {
#endif

struct Pair {
    char *name;
    char *value;
};

int test(struct Pair **pairs);

#ifdef __cplusplus
}
#endif

#endif /*__TEST__*/
