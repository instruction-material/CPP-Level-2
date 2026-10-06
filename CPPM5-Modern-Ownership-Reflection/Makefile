CXX = clang++
override CXXFLAGS += -std=c++20 -Wall -Wextra -Wpedantic -Werror
SRCS = main.cpp
.PHONY: all clean run run-debug
all: main
main: $(SRCS)
	$(CXX) $(CXXFLAGS) $(SRCS) -o "$@"
main-debug: $(SRCS)
	$(CXX) $(CXXFLAGS) -g -O0 -fsanitize=address,undefined -fno-sanitize-recover=all $(SRCS) -o "$@"
run: main
	./main
run-debug: main-debug
	./main-debug
clean:
	rm -rf main main-debug main.dSYM main-debug.dSYM
