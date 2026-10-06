# Two-Dimensional Arrays, Layout, and Function Boundaries

## Purpose and prerequisites

Use initialized built-in arrays, `sizeof`, indexes, nested loops, and CPPM1–2
lifetime/boundary reasoning to explain a grid before implementing operations.
This worked lesson has one C++20 entry point; change a dimension and predict a
new rectangular traversal before using the reference to check the prediction.

## Read, trace, and explain

`int grid[2][3]` has two row objects, each with three integers. Its first index
selects a row; its second selects an element inside that row. Valid row indexes
are 0 and 1; valid columns are 0, 1 and 2. Fill one row at a time with nested
loops. Rows occur in row-major storage order, but a row's int pointer has that
row's array bounds. A cast does not create a new flat array object.

```cpp
int grid[2][3] = {{1, 2, 3}, {4, 5, 6}};
const int flat[6] = {1, 2, 3, 4, 5, 6};
// grid[row][column] selects two objects; flat[row * 3 + column]
// selects an element of one actual six-int array.
```

At a function boundary, `const int rows[][3]` adjusts to a pointer to a
three-int row. The row count is still explicit; the three-column shape is in
the type. It is neither `int*` nor `int**`. The source's `printRows` reads only
the initialized rows supplied by its caller. A separately allocated `int**`
table has independently owned row arrays and may have no adjacent row storage.
See the [C++ draft array rules](https://eel.is/c++draft/dcl.array) and
[pointer-addition rules](https://eel.is/c++draft/expr.add).

In the owning scope, `sizeof(grid) / sizeof(grid[0])` counts rows, and
`sizeof(grid[0]) / sizeof(grid[0][0])` counts columns. These expressions do not
recover a passed pointer's capacity. Establish live storage, initialization,
shape and actual row capacity before a call. Do not execute a bad index to
discover a dimension. The existing ten-by-ten demonstration, assignment to
row 4/column 2, original three-by-three sample, and row-plus-column fill remain.
The added two-by-three sample makes the rectangular case explicit.

## Walkthrough and self-check

Draw two rows of three boxes. Trace the nested loop's first and final cells,
then explain why swapping row and column counts is a different shape. Predict
the original ten-by-ten counts and initialized output. Compare a typed-row
call with the separate real flat array's index formula. An instructor can first
ask which object an index selects, then reveal one row boundary, then trace a
single function call. No invalid pointer cast is needed for the walkthrough.

Completion evidence is a rectangular trace, the owning-scope dimension
expressions, a typed function declaration, a lifetime/capacity statement, and
warning-clean ordinary and sanitizer runs. Proceed to required 2D Array
Practice; Bank Transactions is an optional applied grid.

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
This worked lesson is complete. Predict its traces, save a changed rectangular
attempt, and confirm the outputs before treating the walkthrough as complete.
The course's current-pack link imports current lesson files into a different
project key so an earlier saved attempt remains available.
