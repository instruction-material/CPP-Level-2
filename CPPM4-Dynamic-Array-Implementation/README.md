# Dynamic Array Implementation

## Purpose and project role

This is the required CPPM4 project after the dynamic-variable lifetime lesson
and the ownership and copy-control readiness work. Implement a small integer
container that owns and grows a raw array. Keep the original `DynamicArray.h`,
`DynamicArray.cpp`, `main.cpp`, `addVal`, `printVals`, and `get` interface and the
demonstration that appends the integers 1 through 81. The optional Assembly Line
and Grocery List projects have different application goals; they do not replace
this required container project.

The learner folder is `CPPM4-Dynamic-Array-Implementation-Starter`. The reference
folder is `CPPM4-Dynamic-Array-Implementation`. Both contain this complete brief
and an independent Makefile. The learner has a safe empty constructor placeholder,
provided destruction, unfinished append/resize/observer bodies, and four declared
copy/move operations whose definitions must be written. Its default driver reports
an unfinished append task. Calling the missing operations before implementing them
causes a link error. A successful untouched learner run is not completed work.
Attempt each task and predict its behavior before opening the complete reference.

## Storage, ownership and valid state

The logical size `mySize` counts initialized elements. The capacity `maxSize`
counts allocated integer slots. The invariant is `0 <= mySize <= maxSize`.
At zero capacity, the size is zero and `myVals` is `nullptr`. At positive
capacity, `myVals` is the sole owner of that many live slots allocated by
`new int[capacity]`. Only indexes less than the logical size may be read.
Unused capacity is not initialized data. Pair each allocation with exactly one
`delete[]`, including when its owner is replaced or leaves scope.

The ordinary constructor establishes `DEFAULT_SIZE == 5` slots and zero logical
elements. A copy owns independent storage and the same logical values. A move
transfers the existing allocation without allocating, then leaves the source
empty at zero capacity. That source still has a valid lifetime: it can be
destroyed, assigned, observed as empty, or reused with `addVal`. Destroying a
moved-from object must not release the allocation now owned by the destination.

`std::move` permits the move overload to be selected; it does not itself transfer
storage. The four special members and destructor form the Rule of Five. A
compiler-generated copy of an owning raw pointer would share its address without
establishing two independent owners. Do not use a shallow copy. Self-copy and
self-move assignment preserve the object's values and ownership.

## Tasks and instructor walkthrough

1. Establish the constructor invariant. Draw the empty logical range and five
   available slots. State which slots can be read. The provided destructor is
   compatible with both an allocated array and the empty placeholder.
2. Implement private `resize`. Require a positive capacity at least as large as
   the logical size. Allocate a replacement and copy the initialized elements
   before releasing the old buffer. Integer assignment cannot throw. If allocation
   fails, the original owner, size, capacity and values stay valid and unchanged.
3. Implement `addVal`. When full, grow the capacity before writing the next slot.
   A zero-capacity moved-from array starts again with `DEFAULT_SIZE`, rather than
   attempting to double zero. Other capacities double while representable.
   Check the arithmetic before multiplying and before allocating. Clamp the final
   possible growth to `SIZE_MAX / sizeof(int)`; a full array at that bound throws
   `std::length_error`. This byte bound does not guarantee physical memory.
   Allocation may still throw `std::bad_alloc` or `std::bad_array_new_length`.
   Failed append preserves all existing values and does not increase logical size.
4. Implement the observers. `printVals` writes each logical value followed by
   one space, then one newline; an empty array writes only the newline. `get`
   returns an integer for `index < mySize`. Otherwise it throws
   `std::out_of_range` without writing an error message or changing state. Every
   representable integer, including `-1`, is valid data, so a sentinel cannot
   distinguish that value from an invalid index. An unsigned-converted negative
   index is outside the logical range and is rejected.
5. Define copy construction and copy assignment. Prove that the two owners remain
   independent after either array appends, grows or is destroyed. For assignment,
   retain the destination until replacement allocation and copying succeed.
   Copying a zero-capacity moved-from array produces another reusable empty array.
6. Define move construction and move assignment with their existing `noexcept`
   signatures. Transfer ownership once, release the destination's previous owner
   on assignment, and clear the source's size, capacity and pointer. Prove that
   self-move does not destroy the only owner. No allocation belongs in either move.
7. Keep the original 81-value driver and add separate changed-case drivers for
   copying, moving, reuse and invalid access. Replacing the container with
   `std::vector` skips the manual ownership and growth goal of this project.

For independent study or an instructor walkthrough, use this sequence: predict,
draw both owners and initialized ranges, attempt one operation, run an ordinary
case, run its diagnostic case, and explain a changed case. Useful first hints
are: Which pointer owns the buffer now? Which object's destructor releases it?
What positive capacity follows an empty move source? Which mutation happens
only after an allocation succeeds? Show an attempted trace before comparing
with the reference.

## Acceptance cases

| Case | Required behavior |
| --- | --- |
| Fresh array | Empty logical range; `get(0)` throws; print is one newline |
| Append 1 through 81 | All 81 values retained in order through repeated growth |
| Append `INT_MIN`, `-1`, `0`, `INT_MAX` | Exact values returned; `-1` remains data |
| Index equal to logical size or `SIZE_MAX` | `std::out_of_range`; no output or mutation |
| Copy then append different values at the same next index | Both owners retain their own value |
| Grow or destroy one copy | Other copy still has its independent values |
| Copy assignment into an occupied destination | Old destination replaced; source unchanged |
| Move construct or assign into an occupied destination | Values transferred; source empty and reusable |
| Copy a moved-from source | Both empty owners can be independently reused |
| Self-copy or self-move | Existing logical values preserved |
| Inject failure at construction, copy or full-array growth | Exception; no lost values or leaked array owner |
| Capacity arithmetic near the byte bound | No wrap; positive bounded growth or `std::length_error` |

Use small containers and a fault-injection fixture for allocation failures.
Check capacity arithmetic separately without allocating an enormous array.
Do not manufacture invalid private fields or execute an out-of-bounds read.

## Native and IDE workflow

The site IDE edits, saves, reopens and exports C++; a native C++20 compiler runs
the programs. Use the learner course link when the catalog offers it, confirm
the import, edit the three original files, save an attempt and export its ZIP.
Extract the pack and run:

```sh
make main main-debug
./main
ASAN_OPTIONS=detect_leaks=0 ./main-debug
make clean
```

The Makefile builds explicit sources and rebuilds when the header changes.
It enables strict warnings, treats warnings as errors and adds AddressSanitizer
and UndefinedBehaviorSanitizer to the debug target. Cleanup removes both programs
and macOS diagnostic bundles. LeakSanitizer is disabled in the command for
platform compatibility; this command alone does not prove leak freedom.
The supplied learner reports its pending task in either mode. Completed learner
work must replace all placeholders, define the missing special members and pass
the acceptance cases without pending messages or sanitizer diagnostics.

From the source repository root, the reference/starter build and acceptance gate
is `python3 verify-dynamic-array.py`. It checks ordinary and diagnostic execution,
independent copies, moves, saved values after injected failure, scoped array-owner
cleanup and capacity boundaries. The CMake targets are
`CPPM4_Dynamic_Array_Starter` and `CPPM4_Dynamic_Array_Reference`. Each uses its
own `main.cpp`; do not compile both packs into one executable. The source gate
does not establish that a particular saved IDE attempt is correct or that the
catalog has already imported this new pack.

## Completion evidence

Submit the original 81-value run, implemented container files, an owner and
size/capacity diagram before and after growth, independent copy traces, move
and reuse traces, bounds and failure-case results, and warning-clean ordinary
and sanitizer-clean native run evidence. Include an explanation of why an
observer never reads unused capacity and why cleanup still works after a move.
An additional reflection changes the tested values and traces the same saved
project; it does not require another copy of the implementation.
