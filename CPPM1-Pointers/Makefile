CXX ?= c++
CXXFLAGS ?= -std=c++20 -Wall -Wextra -Wpedantic -Werror

.PHONY: all clean
all: main

main: main.cpp
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) main.cpp $(LDFLAGS) -o $@

main-debug: main.cpp
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -O0 -g main.cpp $(LDFLAGS) -o $@

clean:
	rm -f main main-debug
