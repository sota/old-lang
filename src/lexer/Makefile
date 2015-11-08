.PHONY : test lib clean uptodate

REPOROOT = $(shell git rev-parse --show-toplevel)
NAME := $(notdir $(basename $(shell pwd)))
CXXFLAGS := -std=c++11 -fPIC -O2 -g -Wall -Werror
LDFLAGS := -shared
RAGEL := /usr/local/bin/ragel
RAGELFLAGS := -C

test: lib
	$(CXX) $(CXXFLAGS) test.c -L. -l$(NAME) -o test
	LD_LIBRARY_PATH=. ./test

lib: lib$(NAME).so

lib$(NAME).so: $(NAME).o
	$(CXX) $(LDFLAGS) -o lib$(NAME).so $(NAME).o

$(NAME).o: $(NAME).cpp
	$(CXX) $(CXXFLAGS) -c $(NAME).cpp -o $(NAME).o

$(NAME).cpp: $(RAGEL)
	$(RAGEL) $(RAGELFLAGS) $(NAME).rl -o $(NAME).cpp

clean:
	$(RM) $(NAME).cpp *.o *.so* test

