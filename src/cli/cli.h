#ifndef __SOTA_CLI__
#define __SOTA_CLI__ = 1

#include <array>
#include <string>
#include <stdio.h>
#include <fstream>
#include <iostream>
#include <exception>
#include <sys/stat.h>

#include "tclap/CmdLine.h"

#ifdef __cplusplus
extern "C" {
#endif

int parse(int argc, char **argv);

#ifdef __cplusplus
}
#endif

#endif /*__SOTA_CLI__*/
