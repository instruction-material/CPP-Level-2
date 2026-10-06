# Two-Dimensional Arrays: Extension Challenge

Use `CPPM3-2D-Array-Extension-Starter` for an attempt. The named
`CPPM3-2D-Array-Extension` pack is the completed reference; `REFLECTION.md`
follows the attempt. This optional challenge follows completed required 2D
Array Practice. It adds a checked coordinate boundary and a column statistic,
with its own project and two unfinished task bodies.

## Shape contract and purpose

The observer receives a `const int*` into one real flat, initialized, live int
array with capacity at least `rows * columns`. Draw the logical rectangle and
use the CPPM3 row-major shape. Do not cast a nested row array or `int**` table
to this type. The worked lesson and required practice establish those distinct
object models. The provided `validateGrid` rejects negative dimensions,
unrepresentable extents and detectable null-positive input before access;
actual storage capacity, shape, initialization and lifetime are still caller
preconditions. Explain any false capacity on paper without executing it.

The purpose is to enforce a coordinate boundary before an index calculation and
contrast column aggregation with the row aggregation already completed. Keep
the same stored rectangle; swapping its dimensions changes the interpretation
and is not a transpose implementation. No required-practice body is repeated.

## Two extension tasks

1. `checkedCell` validates the dimensions/storage first, then rejects negative
   coordinates, `row >= rows`, or `column >= columns` with `std::out_of_range`
   before forming an offset or reading a value. After successful checks,
   compute the offset in `std::size_t` and return that one cell. Every empty
   rectangle has no valid coordinate. Preserve all input and retain no pointer.
2. `columnAverages` returns an owning `double*` with one result per **column**.
   Validate dimensions/storage first. Zero columns return null without access
   or allocation. Positive columns with zero rows have no mean and throw
   `std::invalid_argument`. Accumulate each column in `long double`, divide by
   the number of rows in floating point, then return doubles. The caller
   calls `delete[] result` exactly once. Allocation failure propagates before
   an owner is returned. Preserve all input and keep row/column roles explicit.

These are new extension functions, not changes to the four original practice
signatures. A returned observer value has no ownership; a returned averages
array does. Identify that difference before writing code.

## Walkthrough and staged hints

```cpp
const int grid[] = {2, -1, 8, 4, 5, 10};
// Two rows, three columns; predict cell (1, 2) and three column means.
```

Draw the six cells, trace the first/final valid coordinates, and mark the first
invalid row and column. Attempt checked access, then make a two-row column
trace and attempt column averages. An instructor can ask which check precedes
the offset, which indexes belong to one column, how many results are allocated,
and who deletes them. A first hint labels a coordinate; a second labels the
stride between two elements of the same column. Use the reference only after
an attempt and a changed-case self-check.

## Acceptance cases

| Case | Required behavior |
| --- | --- |
| Provided two-by-three rectangle | Cell (1, 2) is 10; three column means are 3, 2, 9 |
| Two rows, one column with 1 and 2 | One double mean of 1.5 |
| One row and several columns | One mean per original cell |
| Negative/first-past/very large coordinates | Reject before offset formation or access |
| Null and zero logical cells | No checked cell; zero columns return null |
| Zero rows and positive columns | No column mean; reject without allocation |
| Negative dimensions or null-positive storage | Reject before access |
| Large positive and negative integers | Floating accumulation; no signed int addition |
| Failed result allocation | Failure propagates; no returned owner or leaked result |

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

Submit two completed bodies, a coordinate-to-offset trace, a column traversal
trace, distinct row/column means for a rectangle, rejected-coordinate evidence,
input-preservation checks and an ownership/cleanup record. Include warning-
clean ordinary and sanitizer runs. This optional challenge complements the
required four calculations and the optional input-ledger model; it has a
distinct current-pack key so an earlier practice attempt remains available.
