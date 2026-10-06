# Matrix Fun with a Matrix Class

This optional CPPM5 project applies class boundaries and value semantics to a
rectangular grid. Preserve the original `Matrix`, `fillMatrix`, `get`, `add`,
`multiply` and `display` tasks. Profile Posts is the principal manual-memory
capstone; this matrix uses `std::vector` for automatic resource ownership.
Level 1 Matrix Addition develops grid algorithms. This parallel Level 2 task
adds an encapsulated representation, multiplication, transactional input,
bounded arithmetic and a comparison of automatic versus manual ownership.

## Packs and prerequisites

Work in `CPPM5-Matrix-Fun-with-Matrix-Class-Starter`; the complete instructor/
reference folder is `CPPM5-Matrix-Fun-with-Matrix-Class`. Each contains the
original `matrix.h`, `matrix.cpp`, `main.cpp`, an independent Makefile and this
identical standalone brief. Attempt one operation and its prediction before
consulting the reference. The starter provides input helpers, safe empty
storage and dimension observers; construction, access, fill, arithmetic,
display, copy assignment and program orchestration remain tasks. Its pending-task output does
not indicate completed work.

Prerequisites: rectangular 2D grids, loops, functions, classes, `std::vector`,
const observers, bounds and native C++20 builds. Profile ownership reasoning
helps explain which resource obligations the standard container removes.

## Representation and contract

A matrix stores rectangular rows in `std::vector<std::vector<int>>`. Derive
dimensions from storage so copied, assigned and moved objects remain safely
observable without stale cached dimensions. The defaulted copy/move constructors
and move assignment use the members' value semantics. Do not add a manual
destructor or raw allocation merely to repeat the Profile exercise. Copy a matrix, refill
one owner and confirm that the other stays independent. Generated moves leave
a valid container; observe the moved-from object through its current shape,
rather than assuming its earlier dimensions still apply. Copy assignment has
one explicit prepare-and-swap step: assigning nested vectors in place can
change earlier rows before a later row allocation throws. Preparing every row
first preserves the destination's old rectangular value on failure. RAII still
handles all allocation cleanup. This domain guarantee explains why that one
operation differs from a pure Rule-of-Zero class with entirely defaulted members.

Accepted constructed shapes are 1 through `MAX_MATRIX_DIMENSION` (20) rows and
columns. `Matrix(0, 0)` is the original empty-result sentinel. Negative,
one-zero and oversized shapes throw `std::invalid_argument` before allocating
grid data. The CLI accepts only positive shapes. This classroom bound limits
input and work; it does not guarantee memory allocation succeeds.

`get` uses **zero-based** row and column indices. Any negative index or index
outside the current shape throws `std::out_of_range`. Values span the native
`int` domain, including zero and negative values. Never use a data value as an
invalid-index sentinel. Display visits stored rows only. Matrix numbers are
diagnostic labels, retained when copied, not unique persistent identities.

`fillMatrix()` reads standard input. The added `fillMatrix(std::istream&)`
overload supplies the same behavior for another stream. Each cell requires
one complete decimal integer line. Whitespace and one optional sign are
accepted; blanks, fractions, suffixes, multiple values and range errors retry
the same cell. EOF or `!quit` throws `MatrixInputStopped`; a read failure throws
`std::runtime_error`. Keep the entire old matrix unchanged if any cell is
unfinished or any allocation/read/output fails before commit. A final line
without a newline is valid input. Supplied parsers preserve output arguments
on rejection.

Addition requires equal shapes and produces their elementwise sum. Incompatible
shapes retain the original diagnostic and return `Matrix(0, 0)` without changing
either input. Multiplication requires the first column count to equal the
second row count and nonempty input shapes; its result is first rows by second
columns. For cell `(i,j)`, traverse `k` from zero through the shared dimension,
combine `first(i,k) * second(k,j)` and accumulate the row-by-column dot product.

Every elementwise sum, individual product and left-to-right partial dot-product
sum must be representable by `int`. Check before computing; otherwise throw
`std::overflow_error`, retaining both inputs. This contract intentionally
rejects an unrepresentable intermediate even if later cancellation would make
the mathematical final result small. It does not silently wrap, clamp or claim
arbitrary-precision arithmetic. Check both negative and positive bounds,
including `INT_MIN * -1`, without performing an unsafe division or negation.

## Program workflow

1. Read the exact complete-line command `add` or `multiply`. `!quit` exits.
2. Read exactly two whole dimensions on one line for each matrix. Retry a
   malformed shape. Retry the pair if the chosen operation is incompatible.
3. Collect each matrix's cells in row-major order, one integer per line.
4. Display the two accepted inputs, then compute and display the result.

EOF or `!quit` at any pending prompt exits zero promptly. It must never loop
on a failed stream or reuse an earlier choice/dimension/element. A stopped
collection displays no partial matrix. A read or arithmetic failure reports
the error and exits one. Extra command-line arguments print usage and exit two.

For a multiplication example, enter:

```text
multiply
2 3
3 2
1
2
3
4
5
6
7
8
9
10
11
12
```

The expected result rows are `58 64` and `139 154`. Predict each dot product
before running. For addition, choose two 2-by-2 inputs with positive, negative
and zero entries and write the expected grid before testing.

## Implementation and instructor checkpoints

1. Validate construction and sketch the rectangular invariant. Explain why
   dimensions should come from storage after a move. Establish zero-filled
   cells for a valid new shape and a safe empty sentinel.
2. Implement bounded access and display. Demonstrate negative row/column,
   row equal to row count and column equal to column count rejections.
3. Fill a separate draft and commit it only once complete. Stop after one
   accepted cell and prove that the old matrix has not changed.
4. Implement addition and multiplication. Explain compatibility before
   allocating the result; use independently calculated expected grids.
5. Implement checked arithmetic for both signs. Record overflow examples
   without executing undefined arithmetic; test rejection in diagnostic builds.
6. Complete the command/dimension workflow with the supplied line helpers.
   Exercise EOF, quit, invalid text, wrong shapes and a recovered valid run.
7. Implement transactional copy assignment, then compare independent copies
   and moved-from observation with Profile's manual
   Rule of Five. Identify the remaining input/domain rules RAII cannot decide.

For independent work or an instructor walkthrough, use the same sequence:
predict, attempt, run, explain the result, then compare with reference material.
Keep the saved attempt and a corrected failure as evidence.

## Native builds and completion

From either pack directory with a native C++20 compiler:

```sh
make main main-debug
./main
./main-debug
make clean
```

Strict warning flags are `-Wall -Wextra -Wpedantic -Werror`; the debug target
adds AddressSanitizer and UndefinedBehaviorSanitizer with immediate diagnostics.
Header dependencies and the `matrix.cpp main.cpp` source list are explicit.
Cleanup removes both executables and macOS diagnostic bundles. The site IDE
edits/saves/exports source; native compilation verifies the exported program.

From the root repository with its required CMake version:

```sh
cmake -S . -B /tmp/cppm5-matrix-build
cmake --build /tmp/cppm5-matrix-build --target CPPM5_Matrix_Class_Starter CPPM5_Matrix_Class_Reference
python3 verify-matrix-class.py
```

Submit the multi-file implementation, strict/debug results, a representation
diagram, compatibility/access/arithmetic tests, complete and interrupted-input
transcripts, copy independence and moved-from observations. Include the known
2-by-3/3-by-2 multiplication, an empty sentinel, one corrected failure and a
short presentation connecting the optional design to the principal capstone.
Further operators, transpose or broader numeric types are optional extensions.
The independent source gate does not complete or certify a saved learner attempt.
