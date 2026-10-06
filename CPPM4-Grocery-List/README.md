# Grocery List

## Purpose and project role

This optional CPPM4 challenge transfers the required integer Dynamic Array to
record data. Keep a `Grocery` struct with name and price, a custom array with
add/print/access operations, and a `GroceryList` menu for add, remove, print and
quit. Preserve the original removal algorithm: build a new array while skipping
one item, then replace the old array. Prepare a short presentation explaining
the program and ownership to an audience of choice. Prices are fictional
exercise data; a `double` and its rounded display are not a financial settlement
or exact currency representation.

The unfinished learner folder is `CPPM4-Grocery-List-Starter`; the complete
reference is `CPPM4-Grocery-List`. Both contain this same standalone brief,
`DynamicArray.h/.cpp`, `GroceryList.h/.cpp`, `main.cpp` and an independent Makefile.
The learner provides safe empty placeholders, destruction, logical-size observation,
input parsers and the original seed demonstration. Its record constructor,
array operations, list operations and menu remain tasks. Four copy/move operations
are declared but intentionally have no definitions: a driver using them cannot
link until those tasks are written. The default run reports the first pending
task, not completed work. Attempt and predict each task before opening the reference.

## Prerequisites, records and valid state

Complete the required integer array and copy-control gate first. A struct is
like a class with public members by default. The overloaded Grocery constructor
initializes a draft's name and price; the default constructor supplies an empty
name and zero price for unused slots. The owning array accepts only names that
contain a non-whitespace character and finite nonnegative prices. Public draft
fields may be edited before insertion. Insertion validates the record before
changing storage. Editing a copy returned by `accessVal` does not alter the
stored record.

`mySize` counts accepted logical records and `maxSize` counts allocated slots.
Maintain `0 <= mySize <= maxSize`. Zero capacity means zero size and a null
pointer. At positive capacity, `myVals` is the sole owner of an array created
by `new Grocery[capacity]`; every slot is an initialized Grocery placeholder.
Only the first `mySize` slots are application data. Pair each array allocation
with exactly one `delete[]`, which also destroys the strings in every slot.
Never read beyond logical size or retain an address into replaced storage.

Copying a Grocery copies its string, which can allocate and throw. A raw
replacement pointer alone does not clean up when the copy constructor throws:
the incomplete DynamicArray's destructor is not called. In the reference, a
temporary `std::unique_ptr<Grocery[]>` owns replacement storage while copies
are attempted. When every copy succeeds, `release()` transfers the pointer
to the raw owning member. Otherwise the temporary destroys the array. This
small RAII bridge protects the manual-memory exercise; a standard container
is the ordinary modern choice after completing the ownership comparison.

## Required tasks for this optional project

1. Complete the overloaded Grocery constructor with member initialization for
   both original fields. Explain the provided default placeholder and why
   unused initialized slots are not part of logical size.
2. Adapt the integer DynamicArray without replacing it with `std::vector`.
   Preserve its original public names: `addVal`, `printVals`, `accessVal` and
   `getSize`. The ordinary constructor allocates `DEFAULT_SIZE == 5` slots.
   `getSize` returns logical size; `printVals` displays that many records with
   item numbers starting at one. `accessVal` uses zero-based indexes and returns
   an independent record copy for `index < mySize`; otherwise it throws
   `std::out_of_range` without output or mutation. Returning an empty Grocery
   would conceal an invalid access, so it is not the error contract.
3. Implement independent copy construction and copy assignment. Keep temporary
   ownership until all string copies succeed, then commit size, capacity and
   pointer. Failed replacement preserves the destination's state. Self-copy
   preserves data. Copying an empty moved-from array produces another reusable
   empty array.
4. Implement allocation-free move construction and move assignment with their
   declared `noexcept` signatures. Transfer the owner once and leave the source
   at zero size, zero capacity and `nullptr`. It remains valid to destroy,
   observe, assign or reuse. Self-move preserves values. Assignment releases
   the destination's previous owner once.
5. Implement resizing and append. Zero-capacity reuse starts with five slots;
   other full capacities double while representable. Check before multiplying,
   clamp the final possible growth to `SIZE_MAX / sizeof(Grocery)`, and reject
   further growth with `std::length_error`. A byte bound does not guarantee
   physical memory or account for every allocator's limits: allocation can
   still fail. Prepare all existing copies and the appended record before
   committing a growth replacement. Assign a non-growing unused slot before
   increasing size. Failures preserve existing logical records and size;
   failed replacement also preserves the old capacity and owner.
6. Complete GroceryList's add/print/remove methods. It composes a DynamicArray,
   so its generated copy and move operations use that member's Rule of Five.
   This is the Rule of Zero for the outer list. `removeItem` accepts one-based
   numbers. Zero or a number larger than size prints rejection without mutation.
   For a valid number, build surviving records in order in a separate array and
   commit only after every copy succeeds. The success message follows the commit:
   an output error at that point does not undo an already completed removal.
7. Complete the menu and reproduce the seed demonstration: add milk at 2.00 and
   print, add cheese at 5.00 and print, add eggs at 3.25, remove item three and
   print. The menu begins with milk and cheese remaining. New interactions
   mutate this list, not a second disconnected example.

For independent study or an instructor walkthrough, predict, draw owners and
initialized ranges, attempt one method, then compare ordinary and diagnostic
runs. First hints ask: Which owner releases a failed replacement? Which string
copy can throw? Which indexes are valid? When does logical size change? Which
list still owns storage after a move? Use an attempted trace before consulting
the reference, and explain unsafe cases on a diagram rather than executing them.

## Menu input and mutation contract

Read complete lines and trim surrounding ASCII whitespace. Preserve spaces
inside item names. Commands are the exact trimmed words `add`, `print`, `remove`
and `!quit`; other commands report rejection without mutation. Blank names retry.
Price is one complete decimal token in the classic locale: a sign, fractional
value or scientific notation is accepted if its result is finite and nonnegative.
Reject blanks, trailing text, second numbers, negative values, NaN, infinity and
overflow, retrying the same item's price. Zero is valid. Parse item numbers as
whole positive decimal values representable by `std::size_t`; an optional leading
plus is allowed, while zero, negatives, fractions, overflow and trailing text retry.
A positive number beyond the current list is rejected by `removeItem` without
mutation and returns to the menu.

The provided parsers leave their output argument unchanged on rejection. Validate
the entire add or remove request before mutating. `!quit` at any pending prompt
exits cleanly without committing that unfinished request. EOF does the same with
status zero; a read error returns one. A final line without a newline is still
input. Do not reuse stale commands, names, prices or indexes after a failed read.
Allocation or record-copy exceptions reach main, report failure and return one;
the stack-owned list releases its buffer on exit. A display failure can follow
a successful mutation, so a missing acknowledgement does not prove it never occurred.

## Acceptance cases and completion evidence

| Case | Required behavior |
| --- | --- |
| Original seed demonstration | Milk and cheese remain after removing eggs |
| Empty list and repeated growth | Zero records is valid; values remain ordered through growth |
| Full name `whole milk` and price zero or a fraction | Exact stored name and accepted finite value |
| Invalid draft or invalid command | Rejection before list mutation |
| Index equal to size or `SIZE_MAX` | `std::out_of_range`; no sentinel or output |
| Copy, then change/grow/destroy one owner | Other owner retains independent records |
| Move construct/assign, then reuse source | Values transferred once; empty source grows safely |
| Self-copy or self-move | Logical records preserved |
| Remove first, middle, last or only item | Survivors stay in order; one-based numbering refreshed |
| Remove zero or a number beyond size | Rejection with unchanged records |
| Allocation or long-string copy failure | Owned replacements cleaned; stated pre-commit data preserved |
| EOF/quit during name, price or item number | No incomplete mutation; clean exit |
| Read error during any prompt | Status one; no stale-data mutation |

Submit the record and container implementations, menu transcripts, independent
copy and move traces, survivor sequences, failure-case results, an owner diagram,
warning-clean and sanitizer-clean native evidence and the short presentation.
The optional reflection explains why string records require a stronger cleanup
plan than integer copies; it extends this saved project rather than importing
another copy of the same program.

## Native and IDE workflow

The site IDE edits, saves, reopens and exports C++; a native C++20 compiler runs
the exported multi-file program. When the catalog offers the new learner action,
confirm the import, edit the original five files, save an attempt and export its
ZIP. Extract the pack and run:

```sh
make main main-debug
./main
ASAN_OPTIONS=detect_leaks=0 ./main-debug
make clean
```

Both builds enable strict warnings as errors; the debug build uses
AddressSanitizer and UndefinedBehaviorSanitizer. Sources and header dependencies
are explicit. Cleanup removes both executables and macOS diagnostic bundles.
LeakSanitizer is disabled for platform compatibility; this command alone does
not prove leak freedom. The untouched learner reports pending work in either
mode; completed work must define every task and pass the acceptance cases.

The root gate is `python3 verify-grocery-list.py`; independent CMake targets
are `CPPM4_Grocery_List_Starter` and `CPPM4_Grocery_List_Reference`. It checks
actual ordinary/debug programs, independent expected records, parser/read-error
boundaries, allocation and string-copy failure cleanup, moves and removal.
Capacity extremes are checked without giant allocations. Source checks do not
certify a particular saved student attempt or completed catalog/IDE integration.
