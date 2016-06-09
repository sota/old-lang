#include "cli.h"

#include <stdio.h>
#include <assert.h>
#include <cstring>
#include <vector>

#include "../version.h"
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

extern "C" struct CliTokens * parse(int argc, char *argv[]) {

    struct CliTokens *tokens = (struct CliTokens *)malloc(sizeof(struct CliTokens));
    assert(tokens != NULL);

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

    tokens->count = tokenlist.size();
    tokens->tokens = (struct CliToken *)malloc(tokenlist.size() * sizeof(struct CliToken));
    copy(tokenlist.begin(), tokenlist.end(), tokens->tokens);

    return tokens;
}

extern "C" int clean(struct CliTokens *tokens) {
    for (int i=0; i<tokens->count; ++i) {
        free(tokens->tokens[i].name);
        free(tokens->tokens[i].value);
    }
    free(tokens);
    return 0;
}

