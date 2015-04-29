#ifndef __SOTA_CLI__
#define __SOTA_CLI__ = 1

#define VERSION "0.1"

#ifdef __cplusplus
extern "C" {
#endif

#include <stdio.h>

struct SotaToken {
    const char *name;
    const char *value;
    size_t line;
    size_t pos;
};

int scan(const char *source, struct SotaToken **tokens);

#ifdef __cplusplus
}
#endif

#endif /*__SOTA_CLI__*/
