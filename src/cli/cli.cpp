#include "cli.h"

#include <string>
#include <fstream>
#include <sstream>
#include <iostream>
#include <algorithm>
#include "tclap/CmdLine.h"
#include <stdio.h>

#include "../version.h"

extern "C" int parse(int argc, char *argv[], struct CliToken **tokens) {
    int result = 0;
    try {
        TCLAP::CmdLine cmdline("sota: state of the art", ' ', VERSION);
        TCLAP::UnlabeledValueArg<std::string> sourceArg(
            "source",       //name
            "sota source",  //desc
            true,           //reqd
            "",             //value
            "text|file",    //typedesc
            cmdline);       //parser

        cmdline.parse(argc, argv);

        std::string source = sourceArg.getValue();
        if (source.empty()) {
            std::cerr << "source must be non-empty text or file" << source << std::endl;
            return 1;
        }

    } catch (TCLAP::ArgException &ae) {
        std::cerr << "error: " << ae.error() << " for arg " << ae.argId() << std::endl;
    }
    return result;
}
