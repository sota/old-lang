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
        TCLAP::UnlabeledValueArg<std::string> sourceArg(
            "source",                       //name
            "sota source <text|file>",      //desc
            true,                           //reqd
            "",                             //value
            "string",                       //typedesc
            cmdline);                       //parser

        cmdline.parse(argc, argv);

        std::string source = sourceArg.getValue();
        if (!source.empty()) {
            std::cout << "source = " << source << std::endl;
        }

    } catch (TCLAP::ArgException &ae) {
        std::cerr << "error: " << ae.error() << " for arg " << ae.argId() << std::endl;
    }
    printf("sota\n");
    return 0;
}
