CXX ?= g++
override CXXFLAGS += -g

SRCS = DynamicArray.cpp main.cpp
TARGET_BASE = main
DEBUG_TARGET_BASE = main-debug

ifeq ($(OS),Windows_NT)
WINDOWS_SHELL := $(notdir $(SHELL))
EXEEXT := .exe
ifeq ($(filter sh.exe bash.exe zsh.exe,$(WINDOWS_SHELL)),)
RUN_PREFIX :=
REMOVE_CMD = del /Q
else
RUN_PREFIX := ./
REMOVE_CMD = rm -f
endif
else
EXEEXT :=
RUN_PREFIX := ./
REMOVE_CMD = rm -f
endif

TARGET = $(TARGET_BASE)$(EXEEXT)
DEBUG_TARGET = $(DEBUG_TARGET_BASE)$(EXEEXT)

.PHONY: all clean run run-debug

all: $(TARGET)

$(TARGET): $(SRCS)
	$(CXX) $(CXXFLAGS) $(SRCS) -o "$@"

$(DEBUG_TARGET): $(SRCS)
	$(CXX) $(CXXFLAGS) -O0 $(SRCS) -o "$@"

run: $(TARGET)
	$(RUN_PREFIX)$(TARGET)

run-debug: $(DEBUG_TARGET)
	$(RUN_PREFIX)$(DEBUG_TARGET)

clean:
	-$(REMOVE_CMD) "$(TARGET)" "$(DEBUG_TARGET)"
