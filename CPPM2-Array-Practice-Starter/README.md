# Array Practice

## Purpose and project role

This is the required CPPM2 project after the array and arithmetic lessons. Keep
all four original tasks: create and print ten perfect squares starting at zero,
compare endpoints, sum integers, and total the sample strings' letters. The raw
array and explicit size are the model under study. The optional verification
drill reuses this completed project for new traces; it is not another required
implementation.

The learner folder is `CPPM2-Array-Practice-Starter`; the reference folder is
`CPPM2-Array-Practice`. Each has one `main.cpp`, a Makefile, and this same brief.
The learner's four task bodies remain unfinished. Its default run reports four
pending tasks, while initialized storage keeps partial attempts defined. The
reference contains completed functions and a separate `REFLECTION.md`. Make an
attempt and predict its behavior before opening the reference.

## Prerequisites and range vocabulary

Read Raw Arrays as Contiguous Memory and Pointer Arithmetic first. A raw array
owns a fixed number of elements for its lifetime. When passed to these functions,
its name supplies a pointer to the first element; the pointer does not carry the
capacity. The explicit `size` is the logical number of elements being processed.
The caller must prove that the storage is live and initialized and that
`0 <= size <= capacity`. An index into that logical range satisfies
`0 <= index < size`. Storage after the logical range is not part of the input.

The provided `validateRange` rejects a negative size and a null pointer paired
with a positive size. It cannot prove capacity, initialization, or lifetime.
A non-null pointer alone proves none of these. Never test an oversized logical
length by accessing outside the real array; describe that caller violation on a
range diagram instead. These functions borrow storage, do not own or resize it,
and do not retain a pointer after returning.

## Four tasks and instructor walkthrough

1. Implement `fillPerfectSquares` for exactly ten writable elements and print
   the array using the provided display loop. The sequence starts with `0 * 0`
   and ends with `9 * 9`. Other lengths are rejected with `std::invalid_argument`.
2. Implement the original `bool firstLast(int arr[], int size)`. For zero logical
   length, return false without reading either endpoint. One element compares
   with itself. For a positive valid range, compare its first and last elements.
3. Implement the original `int sumArray(int arr[], int size)`. Empty input totals
   zero. Process the elements in order. Before each addition, reject a prefix
   total outside `INT_MIN` through `INT_MAX` with `std::overflow_error`. A later
   cancelling value does not make an overflowing earlier addition valid.
4. Implement the original `int sumLetters(std::string words[], int size)`.
   Empty input totals zero. `std::string::size()` counts bytes. For the original
   ASCII words, bytes coincide with letters. Before narrowing or adding each
   size, reject a total that would exceed `INT_MAX` with `std::overflow_error`.
   This exercise does not count Unicode characters or graphemes.

For all three observers, reject negative sizes and null-positive ranges before
access, accept a null pointer with zero size, and preserve every input element.
The square helper is the sole mutator. Keep the original public function names
and parameter/return types. Replacing them with a different container skips the
explicit-boundary reasoning this project is meant to teach.

Use a prediction, range diagram, attempted function, ordinary run, diagnostic
run, and changed-case explanation for each task. An instructor can ask which
owner keeps storage alive, which indexes will be read, and which prefix could
exceed the result type before giving a staged hint.

## Acceptance cases

| Case | Required result |
| --- | --- |
| Ten squares `0, 1, 4, ..., 81` | All ten values printed; endpoints false; integer sum 285 |
| Original words `happy`, `Juni`, `computer` | Total letters 17 |
| Null pointer with size zero | Endpoint comparison false; either sum zero; no access |
| One integer `7` | Endpoints true; sum 7 |
| Values `2, 5, 2`, logical length two | Endpoints false; sum 7; unused third element unchanged |
| Empty strings and one two-byte UTF-8 sequence | Empty strings add zero; the sequence adds two bytes |
| Negative size or null-positive input | `std::invalid_argument` before access |
| `INT_MAX, 1` or `INT_MIN, -1` | `std::overflow_error` before signed overflow |
| `INT_MAX, 1, -1` | Reject the overflowing prefix despite later cancellation |

Explain a length/capacity mismatch without executing it. Large string-count
representability is checked before conversion in the reference; the verification
gate does not allocate gigabytes to exercise that branch.

## Native workflow

The site IDE edits, saves, reopens, and exports C++; compilation uses a native
C++20 compiler. Open the learner link with **Open in IDE**, confirm its import,
save an attempt, and export a ZIP. Extract it and run:

```sh
make main main-debug
./main
ASAN_OPTIONS=detect_leaks=0 ./main-debug
make clean
```

Both ordinary and sanitizer runs must exit successfully without a diagnostic.
The untouched learner reports unfinished tasks and is not a completed exercise.
Complete all four bodies, then confirm that the pending messages disappear and
the acceptance cases pass. Leak detection is disabled for platforms without
LeakSanitizer support; this command does not certify leak freedom.

From the source repository root, run the scoped lesson/project gate:

```sh
python3 verify-array-projects.py
```

Keep an earlier saved attempt. The separate-current-starter link in the course
brief imports the current learner files under a different saved project key.

## Completion evidence

Submit the four implemented tasks, a range/capacity diagram, an endpoint trace,
an ordered-prefix sum table, a string byte-count explanation, acceptance-case
results, and a changed-case explanation. Include warning-clean C++20 build and
sanitizer-clean run evidence. Demonstrate that the three observers leave the
input unchanged. The optional verification drill adds new cases to this saved
work rather than replacing it.
