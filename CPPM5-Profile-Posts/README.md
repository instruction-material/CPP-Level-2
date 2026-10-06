# Profile Posts: manual-memory capstone

This is the principal CPPM5 capstone after dynamic arrays and copy control.
Build a fictional local profile that owns a changing array of `Post` records.
The task combines encapsulation, dynamic capacity, bounds, deep copying,
ownership transfer, input validation and safe cleanup in one complete program.
There is no network connection, real social account or personal-data requirement.

Matrix Class is an optional parallel application of class design and value
semantics. Its `std::vector` storage gives it a different ownership role. It
does not replace this manual-memory exercise. The modern-ownership reflection
compares the completed capstone with standard RAII tools afterward.

## Packs and prerequisites

`CPPM5-Profile-Posts-Starter` is the unfinished learner pack.
`CPPM5-Profile-Posts` is the complete instructor/reference pack. Both contain
`profile.h`, `profile.cpp`, `main.cpp`, `Makefile` and this identical brief.
Keep the original filenames together. Work in the starter and save an attempt
before consulting the reference. Its safe empty constructor and pending-task
messages are scaffolding, not evidence that the task is complete. The four
declared copy/move functions still need definitions before lifecycle drivers
that use them can link.

Prerequisites: arrays, pointers versus owners, heap lifetime, `new[]`/`delete[]`,
classes, constructors/destructors, string records, size versus capacity and the
Rule of Five. Revisit CPPM4 if a pointer alias and a deep copy cannot yet be
distinguished. No package installation is needed; use a C++20 native compiler.

## Model and public contract

Preserve the supplied `Post` and `Profile` interfaces. A `Post` has a caption
and an `int` heart count, defaulting to zero. A stored caption contains at least
one non-whitespace character; a count is between zero and the platform's
`std::numeric_limits<int>::max()`. Display this limit rather than assuming its
width. Test data is fictional, including the original sample captions.

The class owns `Post* myPosts`, logical count `mySize` and capacity `maxSize`.
When capacity is positive, the pointer owns exactly one matching array and
`0 <= mySize <= maxSize`. Only the first `mySize` records are logical posts.
The default capacity is `DEFAULT_SIZE` (five). A moved-from object is a valid
empty owner with zero size/capacity and a null pointer; it can be printed,
copied, assigned, destroyed and appended to again. Positive capacity must be
reestablished on its next append. Check capacity arithmetic before doubling.

`addPost` appends a validated independent record and grows only when full.
`printPost`, `removePost` and `addHearts` take **zero-based API indices**. Printed
post numbers and menu inputs are **one-based**. An invalid API index prints
the supplied diagnostic without changing the profile. Do not subtract one
from a menu number until a positive whole number has been accepted.

`addHearts` accepts a signed change. The final count must stay in the count
domain: a negative result throws `std::invalid_argument`; a result above the
maximum throws `std::overflow_error`. Check before modifying the record, even
for `INT_MIN` and `INT_MAX` changes. Invalid-index diagnostics take precedence.
`sumHearts` returns the exact mathematical total when representable by its
original `int` signature. Otherwise it throws `std::overflow_error` and leaves
all valid individual posts intact. It must not wrap, clamp or silently change
the data. Adding a post rejects invalid data with `std::invalid_argument`.

`removePost` retains the order of surviving posts and preserves capacity.
`fillProfile` is the original duplication extension: repeat the last logical
record through the remaining **current** capacity. It neither grows nor adds
anything when empty. When already full, retain the records and capacity.

Copying creates independent arrays and strings. Copy assignment preserves the
old destination until acquisition/copying succeeds. Moves transfer ownership
without allocating, remain `noexcept`, and empty the source. Self-copy and
self-move assignment preserve the object. Release each acquired array once.

Construction and record mutations must clean up temporary storage if array
allocation or a string copy throws. For failed append, copy assignment,
removal or duplication, the logical records, order, counts and capacity remain
as before the operation. An unused slot is not an accepted post. This is the
strong guarantee for the data mutation. Display/acknowledgment output follows
commit; an output failure afterward does not undo the accepted mutation.
A scoped temporary owner such as `std::unique_ptr<Post[]>` may protect copies
while the class retains its raw-pointer ownership model. Explain the handoff.

## Build and run

From either pack directory:

```sh
make main main-debug
./main
./main --demo
./main-debug
make clean
```

`main` uses C++20 with `-Wall -Wextra -Wpedantic -Werror`. `main-debug` also uses
AddressSanitizer and UndefinedBehaviorSanitizer with immediate failure on a
diagnostic. The source list is `profile.cpp main.cpp`; header edits trigger a
rebuild. Native compilation validates C++ ownership and arithmetic; saving
files in a browser IDE alone does not establish a passing native run.

Default execution begins empty and reads commands until `!quit` or EOF.
`--demo` runs the original finite sample: the three original posts, removal of
the second, ten extra hearts on the first, and five beach posts. The final
state is **seven posts with 160 total hearts**. Other arguments return usage
status two. A pending starter prints the unfinished task; it has not completed
the demo or menu. Unexpected runtime failures report an error and return one.

The repository has independent CMake targets:

```sh
cmake -S . -B /tmp/cppm5-profile-build
cmake --build /tmp/cppm5-profile-build --target CPPM5_Profile_Posts_Starter CPPM5_Profile_Posts_Reference
python3 verify-profile-posts.py
```

Run those commands from the repository root with its required CMake version.
The acceptance script compiles isolated copies of both packs, exercises the
complete reference, injects allocation failures, checks cleanup and input,
then removes temporary builds. It does not complete learner files.

## Command workflow

| Command | Complete-line input and result |
| --- | --- |
| `add` | Nonempty caption, then one nonnegative `int` count; append after both are accepted. |
| `print` | Display all logical posts, including the readable empty profile. |
| `view` | Positive one-based number; show its post or an invalid-index diagnostic. |
| `hearts` | Positive one-based number, then signed `int` delta; validate the resulting count. |
| `remove` | Positive one-based number; remove that post or diagnose an invalid index. |
| `sum` | Report the checked total or its range rejection; preserve records. |
| `fill` | Duplicate the last record to current capacity; optional extension. |
| `!quit` | Exit cleanly, including at a data prompt. |

Whitespace around command/numeric lines is accepted. Numeric input uses the
entire trimmed line, with one optional leading plus sign. Reject blank, fractional,
multi-value, suffixed and out-of-range numbers without reusing an earlier
value. Retry the same field on malformed input. Unknown commands print help.
EOF at any prompt exits zero and discards the incomplete draft. A failed read
exits one with `Input could not be read.` and leaves the in-progress mutation
uncommitted. The supplied numeric parsers are helpers; the starter's menu is a
learner task. Checked count rejections are recoverable menu events.

## Suggested sequence

1. Sketch one empty owner, one populated owner and a moved-from owner. Label
   array ownership, logical size, capacity and observer indices. Write the
   invariants before implementing changes.
2. Implement construction, destruction, validation, append/growth and display.
   Test zero, five, six and many posts, using captions long enough to allocate
   strings independently. Identify exactly when a draft becomes logical data.
3. Implement both copies and both moves. Trace source and destination before
   and after each operation, including self-assignment and moved-from reuse.
   Edit a copy and confirm the source remains independent.
4. Implement removal and heart updates. Remove first, middle, last and sole
   posts. Explain how failed string copies leave the old records unchanged.
   Check negative and maximum arithmetic before storing the result.
5. Complete the line-based menu. Start empty, enter a draft, view/update/remove,
   reject an invalid index and command, and stop mid-draft with EOF or `!quit`.
   Distinguish malformed numbers from accepted numbers outside logical bounds.
6. Add the checked total and duplication extensions. Predict the capacity
   after appending six posts, then test empty, partly full and full duplication.
7. Run strict and sanitizer builds. Record a failing attempt and its correction,
   then compare the saved design with a vector or unique-pointer alternative.

For independent work, keep predictions and observed outputs with the saved
attempt. For instructor walkthroughs, pause at the same checkpoints and have
the learner explain the next owner/state transition before running it.

## Completion and presentation

The core deliverable is the multi-file manual owner and working add/display/
view/heart-update/remove menu with all five lifetime operations. Total hearts
and filling unused slots preserve the original bonus role; their implementations
must meet the same safety contract when included. Further fields, caption
editing and richer statistics are optional extensions after the core works.

Provide the source files, build instructions, an ownership diagram, and brief
evidence for empty/add/view/update/remove, invalid command/index, growth,
independent copies, both moves, self-assignment, moved-from reuse and destruction.
Include the arithmetic boundary cases, an incomplete input case, one corrected
failure and native warning/sanitizer results. Explain what a failed string
copy would preserve and why a printed acknowledgment is after commit.

Present the original demonstration and a separate custom fictional workflow.
Explain which manual obligations `std::vector<Post>` would remove and which
record/menu rules would still be necessary. Preserve the saved attempt before
opening or copying reference material. Reference output is a comparison aid,
not evidence that an unfinished learner implementation has passed.
