#include "cli.h"

#include <string>
#include <sstream>
#include <iostream>
#include <algorithm>
#include "tclap/CmdLine.h"
#include <stdio.h>

extern "C" int parse(int argc, char *argv[], struct CliToken **tokens) {
    printf("parse\n");
    int count = 3;
    *tokens = (struct CliToken *)malloc(count * sizeof(struct CliToken));
    for (int i=0; i<count; ++i) {
        (*tokens)[i].name = "si";
        (*tokens)[i].value = "og";
    }
    return count;
}
/*
int parse(int argc, char *argv[]) {
    printf("cli::parse\n");
    try {
        TCLAP::CmdLine cmdline("sota: state of the art", ' ', "0.1");
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
        std::ostringstream cmd;
        cmd << "./sota-jit \"" << source << "\"";
        system(cmd.str().c_str());

    } catch (TCLAP::ArgException &ae) {
        std::cerr << "error: " << ae.error() << " for arg " << ae.argId() << std::endl;
    }
    return 0;
}
*/

