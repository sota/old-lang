//#include "argtable3.h"

#define VERSION "0.1"

int main(int argc, char **argv) {
/*
    const char *sota = "sota";
    int exitcode = 0;
    int errors = 0;
    struct arg_lit *help    = arg_lit0("h", "help", "print this help and exit");
    struct arg_lit *version = arg_lit0("v", "version", "print the version and exit");
    struct arg_end *end     = arg_end(20);

    void *argtable[] = {
        help,
        version,
        end,
    };

    if (arg_nullcheck(argtable) != 0) {
        printf("%s: insufficient memory for argtable\n", sota);
        exitcode = 1;
    }

    errors = arg_parse(argc, argv, argtable);

    if (help->count) {
        printf("usage: %s", sota);
        arg_print_syntax(stdout, argtable, "\n");
        arg_print_glossary(stdout, argtable, " %-25s %s\n");
        exitcode = 0;
        goto exit;
    }

    if (version->count) {
        printf("sota version: %s\n", VERSION);

        exitcode = 0;
        goto exit;
    }

    if (errors) {
        arg_print_errors(stdout, end, sota);
        printf("try '%s --help' for more info\n", sota);
        exitcode = 1;
        goto exit;
    }

exit:
    arg_freetable(argtable, sizeof(argtable) / sizeof(argtable[0]));
    return exitcode;
*/
    return 0;
}
