#include "cli.h"

void foo() {
    printf("foo: void\n");
}

int bar(int x) {
    printf("bar: x=%d\n", x);
    return x;
}

int baz(int x, const char *text) {
    printf("baz: x=%d text=%s\n", x, text);
    return x;
}

int parse(int argc, char **argv) {
    printf("parse: argc=%d argv=\n", argc);
    for (int i=0; i<argc; ++i) {
        printf("\t%s", argv[i]);
    }
    return argc;
}
