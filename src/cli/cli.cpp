#include "cli.h"

#include <stdio.h>
#include <map>
#include <string>
#include <fstream>
#include <sstream>
#include <iostream>
#include <algorithm>
#include <cstring>

#include "version.h"
#include "docopt.h"

static const char USAGE[] =
R"(
usage:
    sota [options] [<source>]

options:
    -h --help     show this screen
    --version     show version

source:
    text | file

sota is state of the art
)";

extern "C" int parse(int argc, char *argv[], struct CliToken **tokens) {

    auto args = docopt::docopt(
        USAGE,
        {argv+1, argv+argc},
        true,
        SOTA_VERSION);

    std::vector<struct CliToken> tokenlist;
    for(auto const& arg : args) {
        if (arg.second.isString()) {
            char *name = (char *)malloc(strlen(arg.first.c_str()) + 1);
            std::strcpy(name, arg.first.c_str());
            char *value = (char *)malloc(strlen(arg.second.asString().c_str()) + 1);
            std::strcpy(value, arg.second.asString().c_str());
            tokenlist.push_back({
                name: name,
                value: value
            });
        }
    }

    *tokens = (struct CliToken *)malloc(tokenlist.size() * sizeof(struct CliToken));
    copy(tokenlist.begin(), tokenlist.end(), *tokens);

    return tokenlist.size();
}
