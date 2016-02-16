.PHONY : test lib clean uptodate

REPOROOT = $(shell git rev-parse --show-toplevel)
DOCOPTDIR := $(REPOROOT)/src/docopt
NAME := $(notdir $(basename $(shell pwd)))
CXXFLAGS := -std=c++11 -fPIC -O2 -g -Wall -Werror -Wno-unknown-pragmas -I$(DOCOPTDIR)
LDFLAGS := -shared

test: lib
	$(CXX) $(CXXFLAGS) test.c -L. -l$(NAME) -o test
	LD_LIBRARY_PATH=. ./test

lib: lib$(NAME).so

lib$(NAME).so: $(NAME).o docopt.o
	$(CXX) $(LDFLAGS) -o lib$(NAME).so $(NAME).o docopt.o

$(NAME).o: $(NAME).cpp
	$(CXX) $(CXXFLAGS) -c $(NAME).cpp -o $(NAME).o

docopt.o:
	$(CXX) $(CXXFLAGS) -c $(DOCOPTDIR)/docopt.cpp -o docopt.o

clean:
	$(RM) *.o *.so* test

