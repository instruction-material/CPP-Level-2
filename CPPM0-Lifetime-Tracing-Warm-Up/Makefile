all: main

CXX = clang++
override CXXFLAGS += -std=c++14 -Wall -Wextra -pedantic

SRCS = $(shell find . -name '.ccls-cache' -type d -prune -o -type f -name '*.cpp' -print | sed -e 's/ /\\ /g')

main: $(SRCS)
	$(CXX) $(CXXFLAGS) $(SRCS) -o "$@"

main-debug: $(SRCS)
	$(CXX) $(CXXFLAGS) -g -O0 $(SRCS) -o "$@"

clean:
	rm -f main main-debug
