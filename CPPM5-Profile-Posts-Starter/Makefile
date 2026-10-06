CXX = clang++
override CXXFLAGS += -std=c++20 -Wall -Wextra -Wpedantic -Werror
SRCS = profile.cpp main.cpp
HEADERS = profile.h
.PHONY: all clean run run-debug demo
all: main
main: $(SRCS) $(HEADERS)
	$(CXX) $(CXXFLAGS) $(SRCS) -o "$@"
main-debug: $(SRCS) $(HEADERS)
	$(CXX) $(CXXFLAGS) -g -O0 -fsanitize=address,undefined -fno-sanitize-recover=all $(SRCS) -o "$@"
run: main
	./main
run-debug: main-debug
	./main-debug
demo: main
	./main --demo
clean:
	rm -rf main main-debug main.dSYM main-debug.dSYM
