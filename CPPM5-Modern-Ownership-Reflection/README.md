# CPPM5 Modern Ownership Reflection

This supplied worked comparison closes the principal Profile Posts capstone.
It is a reflection and focused transfer activity, not another unfinished
implementation or a replacement for the capstone. Preserve the saved Profile
attempt and compare one owner from it with these smaller examples. Matrix
Class remains an optional parallel design using automatic container storage.

Prerequisites: the capstone's invariants, Rule of Five, deep copy, move, growth
and cleanup guarantees. The fictional score values `84, 91, 76, 88` are the
original fixed demonstration data, not real learner records.

## Predict before running

Write the three expected score sequences and label each owner before reading
the worked program. Predict what happens if output throws after allocation:
Which path releases the array? Does a raw pointer's local lifetime delete the
heap object? Which object already owns automatic cleanup? Keep the prediction
and a first attempted explanation with the saved capstone work.

The ordinary output is:

```text
Manual array: 84 91 76 88
Manual responsibility: delete[] must run exactly once.

Vector: 84 91 76 88
Vector responsibility: the vector cleans up its own storage.

unique_ptr array: 84 91 76 88
unique_ptr responsibility: ownership is still explicit, but cleanup is automatic.
```

Score lines contain a trailing space after the last value. The final newline
is ordinary output, not evidence that cleanup was tested under failure.

## Ownership and exception paths

The manual branch acquires `new int[size]` and releases it with `delete[]`.
The local pointer itself has no destructor that deletes the array. If printing
throws, the catch path releases it and rethrows. If printing succeeds, the
normal path releases it once and sets this pointer to null. The catch and
normal paths cannot both run for the same allocation. Allocation failure
creates no owner and needs no delete. Nulling a pointer does not repair other
aliases or replace deletion.

`std::vector<int>` ties its storage to object lifetime. Its destructor runs
during normal return and stack unwinding. A copy has independent value data;
the container handles resizing and resource cleanup. This removes manual
allocation bookkeeping, not the need for valid heart counts, menu input,
logical indices or domain-specific mutation guarantees.

`std::unique_ptr<int[]>` is a single owner of a heap array. The array form calls
`delete[]` automatically. `get()` passes a non-owning observer to `printScores`;
it does not transfer ownership. A unique pointer cannot be copied as a second
owner; moving transfers ownership. Its size is separate in this example, so
it does not supply vector-style logical growth or bounds checking. `release()`
would give up automatic cleanup and needs an explicit receiving owner.

RAII means resources are tied to an owning object's lifetime. Profile's
temporary array owner applies this principle while the exercise keeps a raw
member. Matrix uses vectors for resources but explicitly prepares copy
assignment to preserve rectangular shape if a later row copy throws. Resource
cleanup and application invariants are related, separate obligations. A
Rule-of-Zero class needs no custom resource special members when its members
already provide the desired lifetime and domain behavior.

## Build and observe

The pack contains complete `main.cpp`, this README and an independent Makefile.
From its directory, with a native C++20 compiler:

```sh
make main main-debug
./main
./main-debug
make clean
```

Both builds use `-Wall -Wextra -Wpedantic -Werror`; the debug target adds
AddressSanitizer and UndefinedBehaviorSanitizer with immediate diagnostics.
Cleanup removes both executables and macOS debug bundles. Unexpected arguments
return usage status two; unexpected runtime failure returns one. Editing and
saving in the site IDE does not perform this native compiler check.

From the source repository root:

```sh
cmake -S . -B /tmp/cppm5-ownership-build
cmake --build /tmp/cppm5-ownership-build --target CPPM5_Modern_Ownership_Reflection
python3 verify-modern-ownership.py
```

The independent source gate compares exact ordinary/debug output, injects
allocation and throwing-output failures in each branch, counts cleanup and
checks the separate CMake target. It does not complete a learner's reflection.

## Focused transfer and instructor walkthrough

1. Preserve the saved capstone attempt, then choose one allocation/growth or
   replacement method. Draw its old owner, temporary owner and commit point.
2. Attempt a short vector or unique-pointer rewrite of that one boundary in
   a separate scratch file. Predict its behavior before consulting this
   worked comparison. There is no need to reimport the entire Profile project.
3. Compare successful execution, allocation failure, record-copy failure and
   output failure. State which data remains accepted and which cleanup still
   belongs to the application. Do not claim RAII alone decides those rules.
4. Explain how copy, move, resizing and destruction responsibilities change.
   Identify a standard container's ordinary production advantage and the
   manual exercise's role in learning lifetime reasoning.
5. Revisit one recorded failure and explain the correction using the owners
   rather than an address alone. Present the prediction, observed output and
   saved code comparison briefly.

For independent reading or an instructor walkthrough, pause before each
branch and explain its normal and exception paths. The supplied complete
program is a comparison aid after the attempted trace.

Completion evidence: a prediction, exact observed sequence, one owner diagram,
one focused attempted rewrite tied to saved capstone work, native results and
an explanation of which responsibilities disappeared and which remain.
Further idiomatic practice belongs in C++ Level 3; deeper custom structures
belong in Data Structures and Algorithms in C++; representation-oriented work
can continue in C Systems Engineering.

## Complete worked program

```cpp
#include <cstddef>
#include <iostream>
#include <memory>
#include <string>
#include <vector>

void printScores(const std::string& label, const int scores[], const std::size_t size) {
    std::cout << label << ": ";
    for (std::size_t i = 0; i < size; ++i) std::cout << scores[i] << " ";
    std::cout << '\n';
}

void manualArrayDemo() {
    const std::size_t size = 4;
    int* scores = new int[size]{84, 91, 76, 88};
    try {
        printScores("Manual array", scores, size);
        std::cout << "Manual responsibility: delete[] must run exactly once.\n";
    } catch (...) {
        delete[] scores;
        throw;
    }
    delete[] scores;
    scores = nullptr;
}

void vectorDemo() {
    const std::vector<int> scores{84, 91, 76, 88};
    std::cout << "Vector: ";
    for (const int score : scores) std::cout << score << " ";
    std::cout << "\nVector responsibility: the vector cleans up its own storage.\n";
}

void uniquePointerDemo() {
    const std::size_t size = 4;
    std::unique_ptr<int[]> scores(new int[size]{84, 91, 76, 88});
    printScores("unique_ptr array", scores.get(), size);
    std::cout << "unique_ptr responsibility: ownership is still explicit, but cleanup is automatic.\n";
}

int main(const int argc, char*[]) {
    if (argc != 1) { std::cerr << "Usage: main\n"; return 2; }
    try {
        manualArrayDemo(); std::cout << '\n';
        vectorDemo(); std::cout << '\n';
        uniquePointerDemo();
        return 0;
    } catch (const std::exception& error) {
        std::cerr << "Ownership comparison stopped: " << error.what() << '\n';
        return 1;
    }
}
```
