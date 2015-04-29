#ifndef __SOTA_CLI__
#define __SOTA_CLI__ = 1

#define VERSION "0.1"

#ifdef __cplusplus
extern "C" {
#endif

struct CliToken {
    const char *name;
    const char *value;
};

int parse(int argc, char *argv[], struct CliToken **tokens);

#ifdef __cplusplus
}
#endif

#endif /*__SOTA_CLI__*/
