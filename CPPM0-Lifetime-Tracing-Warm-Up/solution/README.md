# CPPM0 Project 1: Lifetime Tracing Warm-Up

Trace the provided `ScoreCard` program before changing it. This is an observation
project: the starter is intentionally runnable, and its unfinished work is four
prediction notes and an ownership/lifetime diagram. Use `starter/main.cpp` first;
the separate `solution` contains the program and a reference reflection.

The sample starts with Taylor's score of 70 and creates Morgan's bonus with 100.
Keep the original `ScoreCard`, `printCard`, `updateCopy`, `updateReference`,
`observeConstReference` and `makeBonusCard` names.

## Steps and acceptance checks

1. Before running, predict the score before and after each call. Label the caller
   as owner, the value parameter as an independent object, the reference as an
   alias, and the const reference as a read-only observation.
2. Run the program, record each label and score, and group addresses that identify
   the same object. Explain why editing a copy leaves the caller unchanged and
   editing a reference reaches the caller. The const observer must not mutate it.
3. Complete the four TODO notes and a diagram or table showing mutation points
   and when each observation remains valid. Address numbers and physical stack
   layout vary; automatic storage duration is the language rule.
4. Explain why the returned bonus remains valid. Named return value optimization
   can make `localCard` and the result the same object, so their printed addresses
   may match. A separate result is also permitted. Return by value does not
   return a dangling reference to an ordinary local variable.
5. Optionally compare `-fno-elide-constructors`. Accept both permitted address
   relationships in the ordinary build; do not require exact hexadecimal values.

For an instructor walkthrough, pause for each prediction, draw the alias diagram,
then run and reconcile the evidence. After the core, optionally add a nested scope
and explain which observations must end with it. Keep dangling examples in
comments rather than executing reads through expired references or pointers.

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
