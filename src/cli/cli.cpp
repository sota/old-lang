#include "cli.h"

#include <stdio.h>
#include <map>
#include <string>
#include <fstream>
#include <sstream>
#include <iostream>
#include <algorithm>

#include "docopt.cpp/docopt.h"
#include "../version.h"

/*
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
*/

static const char USAGE[] =
R"(Naval Fate.

    Usage:
      naval_fate ship new <name>...
      naval_fate ship <name> move <x> <y> [--speed=<kn>]
      naval_fate ship shoot <x> <y>
      naval_fate mine (set|remove) <x> <y> [--moored | --drifting]
      naval_fate (-h | --help)
      naval_fate --version

    Options:
      -h --help     Show this screen.
      --version     Show version.
      --speed=<kn>  Speed in knots [default: 10].
      --moored      Moored (anchored) mine.
      --drifting    Drifting mine.
)";

extern "C" int parse(int argc, char *argv[], struct CliToken **tokens) {
    int result = 0;
    auto args = docopt::docopt(
        USAGE,
        {argv+1, argv+argc},
        true,
        VERSION);

    for(auto const& arg : args) {
        std::cout << arg.first <<  arg.second << std::endl;
    }
    return result;
}
