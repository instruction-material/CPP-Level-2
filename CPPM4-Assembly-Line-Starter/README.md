# Assembly Line

## Purpose and project role

This optional CPPM4 transfer project applies the dynamic-variable lesson to
named objects. Keep the original `Object` class, `name`, weight in pounds,
constructor with base/member initialization, and `print` method. Repeatedly
read one object's information, allocate it, print pounds and kilograms using
`kilograms = pounds / 2.205`, and free it before the next object. The original
array bonus remains a distinct optional extension: ask for a count, store all
objects in an array, then print them. Prepare a short presentation explaining
the program and ownership to an audience of choice. This assignment's "BMI"
means base/member initialization.

The unfinished learner is `CPPM4-Assembly-Line-Starter`; the complete reference
is `CPPM4-Assembly-Line`. Both include this same standalone brief and a Makefile.
The learner supplies input helpers and safe placeholders, but its object
constructor, display, dynamic-object helper, primary loop and optional batch
remain tasks. A default learner run reports an unfinished loop. Its successful
build or pending message does not count as a completed project. Predict and
attempt each required task before comparing with the reference. The required
dynamic-array implementation is a separate project with a different goal.

## Prerequisites and object lifetime

Read Dynamic Allocation and Manual Ownership and the pointer/lifetime lessons
first. An automatic variable such as a local string lives until its scope ends.
A dynamically allocated `Object` lives from successful `new Object(...)` until
its owner calls `delete`. Store its address in an owning pointer, use `->` or
`(*pointer).member` only while the object is live, and delete it exactly once.
Releasing the object does not make its old address valid to read. Do not retain
an alias for the next iteration or inspect the freed object.

A member-initializer list initializes `name` and `weight` before the constructor
body. `std::move` can transfer a string into the name member; it does not change
the allocation's ownership. Reject an empty or whitespace-only name and a
negative or non-finite weight. Because the original fields are public, edits
must preserve their data contract; `print` checks it again before display.
The batch array uses a provided default `Object` with an empty name and zero
weight as an initialized placeholder. Only slots filled with accepted input
may be printed. An unfilled placeholder is never a completed named object.

## Input and command contract

Read complete lines. Trim surrounding ASCII whitespace, preserve spaces inside
names, and reserve the whole trimmed line `!quit` for cancellation. A blank
name retries the name prompt. Weight uses one whole decimal token in the classic
locale; surrounding whitespace, a sign, a fractional value and scientific
notation are accepted when the result is finite and nonnegative. Blank input,
trailing text, a second number, negative values, NaN, infinity and overflow
retry the weight for the same name before any object allocation. Zero is valid.
The supplied `parseWeight` leaves its output unchanged on rejection.

EOF at a prompt ends cleanly with status zero. A read error ends with status one.
Never use the previous line or weight after a failed read. A final valid line
without a newline still counts as input. Cancelling or reaching EOF while a
weight is pending discards that incomplete object. Allocation or display
exceptions reach `main`, which reports the failure and returns one. Ordinary
invalid input retries rather than throwing out the whole session.

## Required tasks and instructor walkthrough

1. Implement `Object(std::string, double)` with a member-initializer list and
   the name/weight contract. Keep the default placeholder constructor for the
   optional array. Explain why an uninitialized weight must never be displayed.
2. Implement `print`. Show the full name, weight in pounds, and weight divided
   by `2.205` in kilograms. Preserve the original conversion as the assignment's
   approximation; do not claim that rounded display values are exact measures.
3. Implement `printDynamicObject`. Allocate exactly one `Object`, display it
   and release it on both successful display and a throwing output path. If
   allocation or construction fails, no complete object needs manual deletion;
   the failed `new` expression releases its own storage.
4. Implement the primary `runAssembly` loop. Use the provided `readLine`,
   `trimmed`, `parseWeight` and `LineState` helpers. Complete name and weight
   validation before allocating the object. End or retry according to the input
   contract. Release the current object before asking for the next name.
5. Demonstrate zero, fractional and repeated objects, a name with spaces, invalid
   input followed by correction, and EOF during either prompt. Show one owner
   diagram and a trace of allocation, display and deletion for each iteration.

Work independently or with an instructor by predicting one interaction, drawing
the owner and live object, writing one task, then comparing ordinary and diagnostic
runs. First hints can ask which read succeeded, which value was initialized,
when the object became live, and which cleanup path runs if display throws.
Explain a dangling pointer using a diagram rather than executing a freed read.

## Optional original array bonus

Run the reference with `--batch`. Implement the separate `runBatch` task only
after the one-at-a-time path is correct. The count is a whole decimal number
from 1 through 20, with an optional leading plus sign and surrounding whitespace.
`parseCount` rejects zero, negatives, fractions, overflow and trailing text;
its result is unchanged on rejection. Invalid counts retry before allocation.

Allocate one `Object[count]` array with `new[]`; the default constructor gives
every slot a defined placeholder. Collect and validate each record, assign it
to its slot, and print all records only when the whole batch is ready. Match the
array allocation with `delete[]`, which destroys every slot and its string.
Quit or EOF while collecting cancels the incomplete batch and prints no records.
A read error returns one. Any exception during assignment or output must release
the array before propagating. Do not introduce a second loop that overwrites or
loses the owner. The reference's bound avoids huge allocation requests; it does
not make allocation failure impossible.

## Acceptance and completion evidence

| Case | Required behavior |
| --- | --- |
| `small crate` and `2.205` | Full name, 2.205 pounds and 1 kilogram |
| Weight zero or a valid fraction | Accepted, finite converted value |
| Invalid weight then `4.41` | Retry the same name; create one object with 2 kilograms |
| Two complete records then `!quit` | Each printed once and released before the next |
| Blank name | Retry without allocation |
| EOF or `!quit` at a pending weight | No incomplete object displayed; clean exit |
| Input stream read error | Status one; no stale data reused |
| Constructor/allocation or display failure | Exception reported; owned storage released |
| Batch count invalid then corrected | No allocation for rejected counts |
| Complete batch | Print each accepted record in order after all are stored |
| Cancel a partially filled batch | No records printed; entire array destroyed |

Submit implemented tasks, interaction transcripts, an owner/lifetime diagram,
warning-clean and sanitizer-clean evidence, and the short presentation. Label
bonus evidence separately. The verification fixture injects failures and tracks
scoped allocations; it does not require deliberately enormous real allocations.

## Native and IDE workflow

The site IDE edits, saves, reopens and exports C++; compilation happens with a
native C++20 compiler. When the catalog supplies the new learner action, confirm
its import, edit and save an attempt, and export the ZIP. Extract the pack and run:

```sh
make main main-debug
./main
ASAN_OPTIONS=detect_leaks=0 ./main-debug
./main --batch
make clean
```

Each Makefile names `main.cpp` explicitly, enables strict warnings as errors,
and adds AddressSanitizer/UndefinedBehaviorSanitizer to the debug build.
Cleanup removes both executables and macOS diagnostic bundles. LeakSanitizer
is disabled for platform compatibility; that command alone does not prove
leak freedom. An untouched learner reports pending work in either mode.
Invalid command-line arguments return status two and show the accepted usage.

The root source gate is `python3 verify-assembly-line.py`. Independent CMake
targets are `CPPM4_Assembly_Line_Starter` and `CPPM4_Assembly_Line_Reference`.
Keep their entry points separate. These source checks do not certify a saved
student attempt or establish that the catalog has already wired the new pack.
