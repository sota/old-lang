#include "argtable/argtable3.h"

int main(int argc, char **argv) {
    struct arg_lit *help = arg_lit0(NULL, "help", "print this help and exit");
    struct arg_end *end     = arg_end(20);
    void *argtable[] = {
        help,
        end,
    };
    arg_freetable(argtable, sizeof(argtable) / sizeof(argtable[0]));
    printf("test\n");
    return 0;
}
