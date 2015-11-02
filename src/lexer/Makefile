.PHONY : test lib clean uptodate

REPO_DIR = $(shell git rev-parse --show-toplevel)
RAGEL_DIR := $(REPO_DIR)/src/ragel
RAGEL := $(RAGEL_DIR)/ragel/ragel
NAME := $(notdir $(basename $(shell pwd)))
CXXFLAGS := -std=c++11 -fPIC -O2 -g -Wall -Werror
LDFLAGS := -shared

CWD := `pwd`

test: lib
	$(CXX) $(CXXFLAGS) test.c -L. -l$(NAME) -o test
	LD_LIBRARY_PATH=. ./test

lib: lib$(NAME).so

lib$(NAME).so: $(NAME).o
	$(CXX) $(LDFLAGS) -o lib$(NAME).so $(NAME).o

$(NAME).o: $(NAME).cpp
	$(CXX) $(CXXFLAGS) -c $(NAME).cpp -o $(NAME).o

$(NAME).cpp: $(RAGEL)
	$(RAGEL) $(NAME).rl -o $(NAME).cpp

$(RAGEL): uptodate
	(cd $(RAGEL_DIR) && ./autogen.sh)
	(cd $(RAGEL_DIR) && ./configure --prefix=$(CWD))
	(cd $(RAGEL_DIR) && make)

uptodate:
	test -s $(RAGEL_DIR)/autogen.sh || { echo "is submod (${RAGEL_DIR}) up to date?"; }

clean:
	$(RM) *.o *.so* test

