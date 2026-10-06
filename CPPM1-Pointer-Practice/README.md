# Pointer Practice Lab

## Purpose and project role

This optional choice provides more tracing practice after the required Pointer
Starter. It develops traversal, meeting pointers, and separate scanner/result
cursors before raw-array work. Complete it when pointer movement needs another
exercise; it is not a second required introduction to pointer syntax.

The learner pack is `CPPM1-Pointer-Practice-Starter`; the reference pack is
`CPPM1-Pointer-Practice`. Both contain one `main.cpp` and a Makefile. Implement
the three unfinished functions in the starter before opening the reference's
completed source or `REFLECTION.md`. The original `question3(const std::string&)`
interface and the three original sample inputs are retained.

## Prerequisites and vocabulary

An array stores adjacent elements. `.data()` gets its first-element address;
a `std::array` object itself is not an element pointer. Pointer increments count
elements, not bytes. Within one array, an observer may name an element or the
one-past-end position; only elements can be dereferenced. Relational pointer
comparisons require the same array. `std::size_t` includes zero and cannot
represent a negative length. `sizeof(vector)` measures the vector object, not
the length of its owned buffer. Use the logical character count for traversal.

## Three questions

1. Fill a 20-element `std::array<int, 20>` with 0 through 19. Starting two
   observers at `.data()`, perform ten iterations. Print the first observer's
   current value and advance it by one; print the second's current value and
   advance it by two. Predict all read positions and final positions before
   running. Explain the difference between reading before and after increment.
   The reference keeps Debug 1a/1b/1c disabled: classify their type errors first,
   then explain any remaining skipped element or invalid dereference after
   correcting the types. Do not execute the invalid loop variants.
2. Copy a supplied string into a character vector and add a null terminator for
   printing. Place observers at the first and last logical characters. Move
   the first forward once, check for equality, then move the second backward
   once only if they have not met. Print their visited characters and move
   counts. A single character needs zero moves. Empty input reports absence
   before forming a last-character pointer. Check odd and even lengths; exclude
   the terminator from the logical range. Keep the vector alive and do not
   resize or mutate its buffer while observing it.
3. Implement `question3` twice, once with a result index and once with a result
   pointer. A separate scanner visits input characters left to right, one at a
   time. Start the result at offset zero. Each ASCII digit moves the result by
   that individual digit's value; zero moves it by zero. Non-digits leave the
   result unchanged while the scanner continues. If the next move would reach
   or pass the logical end, stop the whole scan before moving. Empty input
   reports absence and returns without dereferencing. Both implementations
   report the same final character and offset. Borrow the input only during
   the call; do not modify it or retain a pointer after its lifetime ends.

Question 3 uses two independent cursors, not a cursor that reads only the
characters it jumps to. `12` is two digits, not the number twelve. This preserves
the original scan-all algorithm and resolves the ambiguous original wording.
For a nonempty string, prove `offset < length` throughout the loop. Test a move
with `increment < length - offset` to avoid overflowing an unsigned addition.

## Attempt, walkthrough, and self-checks

Predict addresses as offsets into their owner, not fixed numeric addresses.
Draw the scanner and result separately, implement one question at a time, then
compare prediction with observations. An instructor can use the same sequence,
asking which object owns the storage and which position can be read next.

Use these acceptance cases as specifications, not code to copy:

| Case | Required observation |
| --- | --- |
| Question 1, 0 through 19 | First reads 0 through 9; second reads 0,2,...,18 |
| Question 2, empty string | Absence message; no last-character pointer formed |
| Question 2, `x`, `abc`, `abcd` | Move counts 0/0, 1/1, and 2/1 respectively |
| Question 3, `1hello`, `3hello`, `12e4woah` | Final offsets 1, 3, and 7 |
| Question 3, `1a2bc` | Final offset 3, character `b`; scanner continues after `a` |
| Question 3, `0a1b` | Final offset 1, character `a`; zero does not trap the scanner |
| Question 3, `4abc1` | Final offset 4; the next move stops before one-past-end |
| Question 3, `4abc` or `9a1bc` | Final offset 0; an invalid move ends the whole scan |
| Question 3, `abc`, `0`, or `9` | Final offset 0; no invalid dereference |
| Question 3, empty string | Absence message; no result pointer formed |

Add a changed case containing a non-digit byte and show both implementations
agree without altering the input. Explain why a valid one-past-end position in
Question 1 is not permission to dereference it.

## Native workflow

The site IDE edits, saves, reopens, and exports C++; it does not compile or
execute it. Open the learner link with **Open in IDE**. Confirm the source
import, save the attempt, and export a ZIP. Extract that pack and use a native C++20
compiler and Make. An existing saved project retains its work; import the new
starter separately using the fresh-starter link in the course brief after saving
the old attempt.

```sh
make main main-debug
./main
ASAN_OPTIONS=detect_leaks=0 ./main-debug
```

The untouched learner prints three pending-task messages and exits successfully.
Replace the unfinished bodies; do not claim completion until those messages
disappear and all acceptance cases pass. Both completed ordinary and sanitizer
runs must be clean. Leak detection is disabled for platforms where LeakSanitizer
is unavailable; this is not a leak-freedom certification.

From the repository root, verify the independent native source contracts:

```sh
python3 verify-pointer-projects.py
```

## Completion evidence

Submit the three functions, a Question 1 offset table, odd/even/empty traces for
Question 2, a separate scanner/result table for Question 3, acceptance-case
results for both implementations, and a changed-case explanation. Include the
warning-clean C++20 build and sanitizer-clean run. Keep disabled Debug examples
as reasoning prompts rather than enabling undefined behavior in a normal run.
