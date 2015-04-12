#include "cli.h"

int parse(int argc, char **argv) {
    printf("parse: argc=%d argv=\n", argc);
    for (int i=0; i<argc; ++i) {
        printf("\t%s\n", argv[i]);
    }
    return argc;
}
