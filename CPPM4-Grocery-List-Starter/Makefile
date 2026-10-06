CXX = clang++
override CXXFLAGS += -std=c++20 -Wall -Wextra -Wpedantic -Werror
SRCS = DynamicArray.cpp GroceryList.cpp main.cpp
HEADERS = DynamicArray.h GroceryList.h
.PHONY: all clean run run-debug
all: main
main: $(SRCS) $(HEADERS)
	$(CXX) $(CXXFLAGS) $(SRCS) -o "$@"
main-debug: $(SRCS) $(HEADERS)
	$(CXX) $(CXXFLAGS) -g -O0 -fsanitize=address,undefined -fno-sanitize-recover=all $(SRCS) -o "$@"
run: main
	./main
run-debug: main-debug
	./main-debug
clean:
	rm -rf main main-debug main.dSYM main-debug.dSYM
