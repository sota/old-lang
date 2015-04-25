//#include "argtable3.h"

#include <stdio.h>
#include <stdlib.h>
#include <string>
#include <iostream>
#include <algorithm>
#include "tclap/CmdLine.h"

#define VERSION "0.1"

int main(int argc, char **argv) {
    try {
        TCLAP::CmdLine cmdline("sota: state of the art", ' ', "0.1");
        TCLAP::ValueArg<std::string> nameArg("n", "name", "name", true, "scott", "string", cmdline);
        TCLAP::SwitchArg sexArg("s", "sex", "sex", cmdline, false);

        cmdline.parse(argc, argv);

        std::string name = nameArg.getValue();
        bool sex = sexArg.getValue();
        if (sex) {
            std::cout << "sex please" << std::endl;
        }
        if (!name.empty()) {
            std::cout << "name = " << name << std::endl;
        }

    } catch (TCLAP::ArgException &ae) {
        std::cerr << "error: " << ae.error() << " for arg " << ae.argId() << std::endl;
    }
    printf("sota\n");
    return 0;
}
