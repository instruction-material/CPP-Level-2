CXX = clang++
override CXXFLAGS += -std=c++20 -Wall -Wextra -Wpedantic -Werror
.PHONY: all clean run run-debug
all: main
main: main.cpp
	$(CXX) $(CXXFLAGS) main.cpp -o "$@"
main-debug: main.cpp
	$(CXX) $(CXXFLAGS) -g -O0 -fsanitize=address,undefined -fno-sanitize-recover=all main.cpp -o "$@"
run: main
	./main
run-debug: main-debug
	./main-debug
clean:
	rm -rf main main-debug main.dSYM main-debug.dSYM
