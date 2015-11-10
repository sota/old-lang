
CXXFLAGS := -std=c++11 -fPIC -O2 -g -Wall -Werror -I.
LDFLAGS := -shared

test-c: libtest.so test.c
	$(CXX) $(CXXFLAGS) test.c -L. -ltest -o test-c

libtest.so: test.o
	$(CXX) $(LDFLAGS) -o libtest.so test.o

test.o: test.h test.cpp
	$(CXX) $(CXXFLAGS) -c test.cpp -o test.o

clean:
	git clean -xfd
