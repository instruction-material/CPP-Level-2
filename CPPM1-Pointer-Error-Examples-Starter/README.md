# Pointer Error Examples

## Purpose and project role

This optional challenge follows the ten-question Pointer Starter. The goal is
to classify seven pointer failures, establish the missing validity condition,
and demonstrate a correction. A crash alone does not identify a bug, and a
successful run does not prove an invalid access is valid.

The learner pack is `CPPM1-Pointer-Error-Examples-Starter`; the reference pack is
`CPPM1-Pointer-Error-Examples`. Both contain one `main.cpp` and a Makefile.
The starter leaves `repairedExamples()` unfinished. Its ordinary run reports
that work is pending. The reference contains completed corrections and a
separate `REFLECTION.md`. Attempt the explanations before opening the reference.

## Prerequisites and vocabulary

Read the module's pointer and lifetime lessons first. An owner controls cleanup;
an observer stores an address without acquiring ownership. A dereference needs
a live object of the correct type with an initialized value. `nullptr` names no
object. A non-null pointer can dangle after its target's lifetime ends. Setting
one pointer to null does not repair other aliases. Initializing a pointer does
not initialize its target, and declaring `int* first, second` makes only the
first variable a pointer.

## Learner work and instructor walkthrough

1. Keep all seven counterexamples in the block comment disabled. For each,
   record the declared types, owner, observers, object lifetime, first invalid
   operation, and whether the problem is ill-typed code or undefined behavior.
2. Classify dangling access, null dereference, mixed declarators, an uninitialized
   pointer, assigning an integer to a pointer, reading an uninitialized target,
   and incompatible pointed-to types. Do not guess a numeric address or require
   undefined behavior to produce a particular output.
3. Implement `repairedExamples()` with one defined correction per category.
   Preserve the disabled examples for comparison. Use automatic objects where
   possible; if an example allocates, identify its sole owner and clean up once.
4. Predict the corrected values and alias relationships before running. Add a
   changed value and an absent observer case, then explain why both remain valid.
5. With a supported sanitizer build, run each explicit diagnostic once. Record
   the first invalid operation and diagnostic category, then return to the
   ordinary corrected run. The diagnostic modes are deliberately invalid and
   are not acceptance tests for the corrected examples.

An instructor can follow the same sequence: prediction, types and lifetime
diagram, attempted correction, diagnostic, changed-case check, explanation.
The learner owns the prediction and correction; the instructor supplies staged
hints about the target object and its lifetime.

## Native workflow

The site IDE edits, saves, reopens, and exports C++ files; it does not compile
or execute C++. Open the learner link with **Open in IDE**, confirm the source
import, save an attempt, and export its ZIP. Extract the pack, then use a native
C++20 compiler and Make. Keep an existing saved attempt; the new starter can be
opened separately using the fresh-starter link in the course brief after saving
that attempt.

```sh
make main main-debug
./main
ASAN_OPTIONS=detect_leaks=0 ./main-debug
```

Both ordinary runs must exit successfully with no sanitizer report. The untouched
starter explicitly reports unfinished work; it is not a completed submission.
After implementing the corrections, that message must disappear.

```sh
ASAN_OPTIONS=detect_leaks=0 ./main-debug --null
ASAN_OPTIONS=detect_leaks=0 ./main-debug --dangling
```

These two commands are expected to exit unsuccessfully. With the supplied
Makefile, `--null` reports a null store via UBSan; `--dangling` reports
`heap-use-after-free` via AddressSanitizer. Exact wording and exit status vary
by compiler/platform. Ordinary builds reject these flags without making the
invalid access; unknown arguments are also rejected. Do not enable the invalid
examples in an ordinary build. Leak detection is disabled here for platforms
where LeakSanitizer is unavailable; these checks do not certify leak freedom.

From the repository root, run the independent source gates:

```sh
python3 verify-pointer-projects.py
```

## Completion evidence

Submit seven classifications and corrections, an owner/observer diagram for the
dangling case, predicted and observed defined values, one changed-case check,
and the two explicit diagnostic categories. Finish with warning-clean C++20
builds and a sanitizer-clean ordinary run. Explain why a null check cannot prove
that a non-null pointer still names a live object.
