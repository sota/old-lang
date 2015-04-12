#ifndef __SOTA_CLI__
#define __SOTA_CLI__ = 1

#include <stdio.h>

void foo();
int bar(int x);
int baz(int x, const char *text);

int parse(int argc, char **argv);

#endif /*__SOTA_CLI__*/
