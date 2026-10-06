# CPPM0 Project 2: Ownership Boundary Debugging

Compare copies, mutating references and borrowed observations, then complete the
selection helper. Begin with `starter/main.cpp`, whose copy/reference examples
are runnable but whose selection logic is unfinished. The separate `solution`
contains the complete program and reflection. Deliver the finished helper,
three prediction notes and an owner/borrower diagram.

The sample entries have severities 2, 4 and 8. Both editing helpers add 5 to their
parameter; these sample values fit in `int`. Preserve the original `LogEntry`,
`editCopy`, `editCallerOwnedEntry` and `highestSeverity` interfaces.

## Contract and steps

1. Predict the first entry's value and address around each editing call. Explain
   why a value parameter can change independently and a reference can mutate
   the caller's object. Run and reconcile the first two TODO notes.
2. Keep `const LogEntry& highestSeverity(const std::vector<LogEntry>& entries)`.
   Return the earliest entry with maximum severity without copying, editing or
   reordering the vector. Single entries, equal maxima and negative values must
   work. Empty input throws `std::invalid_argument` before indexing; the starter
   already provides that guard and safely reports unfinished nonempty selection.
3. Implement the remaining selection loop. Run the sample, verify the returned
   reference identifies a vector element, and check that selection makes no
   mutation. Try one entry, tied maxima, negatives and an empty vector in a small
   harness, catching the documented empty-input exception.
4. Complete the last TODO and diagram. The vector owns its elements; a const
   reference neither transfers ownership nor extends their lifetime. Reallocation
   invalidates element references. Erasure at or before the selected position,
   clearing or destruction can also invalidate the borrow. Reacquire it after
   such changes. If severities change, recompute the selection even when the old
   reference is still valid. Keep invalidation counterexamples in comments.

For an instructor walkthrough, pause at each call for an ownership sentence and
prediction before running. Review the empty-input contract and borrow lifetime
before the completed selection. As an optional extension, add a const-reference
observer and explain why const cannot rescue an expired borrow. Keep any added
mutation increments representable in `int`.

## Native workflow

Open `starter` in a C++ editor, or confirm its import in the site's code workspace
and export the saved files for a native build. From that folder, run:

```sh
make
./main
make main-debug
./main-debug
make clean
```

Use `make CXX=g++` for GCC. A direct build is
`clang++ -std=c++20 -Wall -Wextra -Wpedantic -Werror main.cpp -o main`.
The parent Makefile builds only its original reference. Keep parent, learner and
reference programs as separate executables. From the repository root,
`python3 verify-lifetime-projects.py` checks these two projects, including their
separate Make/CMake targets and sanitizers. It does not certify every Level 2 pack.
