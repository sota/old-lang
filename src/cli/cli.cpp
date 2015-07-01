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

static const char USAGE[] =
R"(sota: state of the art

    Usage:
      sota <source>
      sota (-h | --help)
      sota --version

    Options:
      -h --help     Show this screen.
      --version     Show version.
)";

extern "C" int parse(int argc, char *argv[], struct CliToken **tokens) {
    auto args = docopt::docopt(
        USAGE,
        {argv+1, argv+argc},
        true,
        VERSION);

    std::vector<struct CliToken> tokenlist;
    for(auto const& arg : args) {

        if (arg.second.isString()) {
            tokenlist.push_back({
                name: (char *)arg.first.c_str(),
                value: (char *)arg.second.asString().c_str()
            });
        }
    }

    *tokens = (struct CliToken *)malloc(tokenlist.size() * sizeof(struct CliToken));
    copy(tokenlist.begin(), tokenlist.end(), *tokens);

    return tokenlist.size();
}
