#ifndef __SOTA_CLI__
#define __SOTA_CLI__ = 1

#ifdef __cplusplus
extern "C" {
#endif

struct CliToken {
    char * name;
    char * value;
};
extern __attribute__((visibility("default")))
int parse(int argc, char *argv[], struct CliToken **tokens);

#ifdef __cplusplus
}
#endif

#endif /*__SOTA_CLI__*/
