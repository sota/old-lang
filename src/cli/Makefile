.PHONY : test lib clean uptodate

REPO_DIR = $(shell git rev-parse --show-toplevel)
DOCOPT_DIR := $(REPO_DIR)/src/docopt
NAME := $(notdir $(basename $(shell pwd)))
CXXFLAGS := -std=c++11 -fPIC -O2 -g -Wall -Werror -I$(DOCOPT_DIR)
LDFLAGS := -shared

test: lib
	$(CXX) $(CXXFLAGS) test.c -L. -l$(NAME) -o test
	LD_LIBRARY_PATH=. ./test

lib: lib$(NAME).so

lib$(NAME).so: $(NAME).o docopt.o
	$(CXX) $(LDFLAGS) -o lib$(NAME).so $(NAME).o docopt.o

$(NAME).o: uptodate $(NAME).cpp
	$(CXX) $(CXXFLAGS) -c $(NAME).cpp -o $(NAME).o

docopt.o: uptodate
	$(CXX) $(CXXFLAGS) -c $(DOCOPT_DIR)/docopt.cpp -o docopt.o

uptodate:
	test -s $(DOCOPT_DIR)/docopt.h || { echo "is submod (${DOCOPT_DIR}) up to date?"; }

clean:
	$(RM) *.o *.so* test

