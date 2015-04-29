#ifndef __SOTA_CLI__
#define __SOTA_CLI__ = 1

#define VERSION "0.1"

#ifdef __cplusplus
extern "C" {
#endif

struct CliToken {
    char *name;
    char *value;
};

struct CliTokens {
    long count;
    struct CliToken tokens[];
};

struct CliTokens parse(int argc, char *argv[]);

#ifdef __cplusplus
}
#endif

#endif /*__SOTA_CLI__*/
