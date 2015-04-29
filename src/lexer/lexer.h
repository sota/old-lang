#ifndef __SOTA_CLI__
#define __SOTA_CLI__ = 1

#define VERSION "0.1"

#ifdef __cplusplus
extern "C" {
#endif

struct SotaToken {
    char *name;
    char *value;
    long line;
    long pos;
};

struct SotaTokens {
    long count;
    struct SotaToken tokens[];
};

struct SotaTokens scan(const char *source);

#ifdef __cplusplus
}
#endif

#endif /*__SOTA_CLI__*/
