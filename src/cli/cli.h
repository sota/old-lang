#ifndef __SOTA_CLI__
#define __SOTA_CLI__ = 1

#ifdef __cplusplus
extern "C" {
#endif

struct CliToken {
    char * name;
    char * value;
};

struct CliTokens {
    int count;
    struct CliToken *tokens;
};

struct CliTokens * parse(int argc, char *argv[]);
int clean(struct CliTokens *tokens);

#ifdef __cplusplus
}
#endif

#endif /*__SOTA_CLI__*/
