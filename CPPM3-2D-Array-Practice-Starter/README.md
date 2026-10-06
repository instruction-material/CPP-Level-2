# 2D Array Practice

Use `CPPM3-2D-Array-Practice-Starter` for an attempt. The named
`CPPM3-2D-Array-Practice` pack is the completed reference; its `REFLECTION.md`
belongs after the attempt. Both packs
carry this same brief and one independent `main.cpp`.

## Purpose and prerequisites

Practice row/column reasoning through four original tasks: an integer sum,
minimum, multiplication table, and one double average per row. Use the CPPM1
range and lifetime rules, CPPM2 traversal and ordered-prefix checks, nested
loops, integer limits, and the ownership framing from CPPM0. The provided
cleanup helper is available so the returned table has a defined owner.

## Shape and storage contract

Draw a rectangle with `m` rows and `n` columns. A row-major flat index is
`row * n + column`. Here the observer's `int*` points into **one actual flat
int array**, initialized and alive for at least `m * n` elements. The driver
preserves the original sample values using:

```cpp
int arr[] = {1, 2, 3, 4, 5, 6, 7, 8, 0};
// Interpret this real nine-element array as three rows and three columns.
```

A built-in `int rows[3][3]` is an array of three row-array objects. Use
`rows[row][column]` or a pointer to a three-int row with that object. Casting
it to `int*` does not establish one nine-int array or allow pointer arithmetic
to cross the first row's bounds. A table of `int*` row pointers is a third
shape: each separately allocated row needs its own cleanup. Do not cast among
these three models. The worked lesson demonstrates the first two explicitly.
The [C++ draft array rules](https://eel.is/c++draft/dcl.array) and
[pointer-addition rules](https://eel.is/c++draft/expr.add) describe these bounds.

The provided `validateGrid` rejects negative dimensions, unrepresentable
element/storage extents, and detectable null-positive input before access.
It cannot prove actual capacity, shape, initialization or lifetime; establish
those caller preconditions with a diagram instead of executing a bad range.

## Four required tasks

1. `sumArray(int*, int, int)` returns an `int` sum in row-major order. An empty
   logical grid returns zero without access. Reject an unrepresentable ordered
   prefix with `std::overflow_error` **before** adding, even if a later element
   would cancel it. Keep every input value unchanged.
2. `minArray(int*, int, int)` returns the minimum of a nonempty grid. Reject an
   empty grid with `std::invalid_argument` before reading its first element.
   Validate dimensions and detectable null first. Preserve the input.
3. `multTable(int N)` returns `int**`, with `N` rows of `N` cells for the original
   1-through-N multiplication table. Reject negative N; zero returns null.
   Reject N when `N * N` cannot fit an `int`, using division before any
   multiplication/allocation. Value-initialize the outer row-pointer array.
   If a row allocation throws, release every allocated row and the outer
   array, then rethrow. The caller calls `deleteTable(result, N)` exactly once.
4. `averageArray(int*, int, int)` returns an owning `double*` with one average
   per row, as the original task requests. Zero rows return null. Positive
   rows with zero columns have no mean and must be rejected. Convert values to
   a floating accumulator before addition and divide in floating point; an
   integer quotient discards fractions before assignment to a floating type.
   Use `long double` for the accumulator and convert each final result to
   `double`. The caller calls `delete[] result` once. Preserve all input values.

The original function names and `int*` observer/dimension model remain. The
average return type is corrected from `float*` to the originally requested
`double*`. This exercise keeps explicit bounds and ownership; replacing every
task with a container operation skips that reasoning.

## Walkthrough and staged hints

Predict the original sample's outputs, draw each row boundary, then implement
one task and test a changed rectangle. An instructor can ask which object an
index belongs to, which values are read, where a prefix could overflow, and who
owns each allocation. If a task is stuck, first mark the loop bounds, next
identify the checked accumulator or allocation owner, then trace one changed
input. Keep completed implementations and reference reflection until after an
attempt and self-check.

## Acceptance cases

| Case | Required behavior |
| --- | --- |
| Original three-by-three sample | Sum 36, minimum 0, row averages 2, 5, 5 |
| One row with 1 and 2 | A double average of 1.5 |
| Two rows with negative values | Correct per-row averages and minimum; input preserved |
| Null pointer, zero logical cells | Sum zero; minimum rejected; zero-row averages null |
| Positive rows, zero columns | Sum zero, no minimum, no defined row averages |
| Negative dimensions or null-positive input | Reject before access |
| `INT_MAX, 1, -1` | Sum rejects the overflowing prefix; row mean uses floating arithmetic |
| N equal to 0, 1, and 5 | Null empty table; correct one-cell and full five-by-five tables |
| Negative N or an unrepresentable largest table cell | Reject before allocation |
| Each allocation failure during a small table | Previously allocated rows and outer array released |

Do not allocate the largest representable table merely to test the arithmetic
boundary. Record a prediction and verify the rejection immediately above it.
An allocation can still fail for a valid size; the caller receives that failure.

## Native workflow

The site IDE edits, saves, reopens, and exports C++. Compilation uses a native
C++20 compiler. Select **Start in IDE**, confirm the import, save an attempt,
export a ZIP, extract it, and run:

```sh
make main main-debug
./main
ASAN_OPTIONS=detect_leaks=0 ./main-debug
make clean
```

Both builds must be warning-clean and diagnostic runs must have no sanitizer
report. Leak detection is disabled for platforms without LeakSanitizer support;
this command alone does not prove that every allocation was released. The
scoped gate separately tracks table allocation failures and cleanup.

From the source repository root, run `python3 verify-2d-array-projects.py`.
The untouched learner reports its pending tasks and exits safely. Complete the
task bodies before treating its successful exit as exercise completion. Use the
course's current-pack link to keep an earlier saved project and import the
current files into a different project key.

## Completion evidence

Submit four completed bodies, a row/column and object-boundary diagram, a sum
prefix trace, a fractional-average case, and a cleanup ledger for ordinary and
failed table construction. Include rectangular, empty, null, negative, integer
boundary and input-preservation checks, plus native build/run evidence. The
optional extension adds a column statistic to this saved attempt; it does not
repeat the four required calculations or reset the project.
