# Pointer Arithmetic and Offset Reasoning

## Purpose and prerequisites

This CPPM2 worked lesson follows Raw Arrays as Contiguous Memory and supports
Array Practice. It explains element offsets and one-past boundaries with the
same twenty initialized integers using both indexing and pointer traversal.
Read the owner/observer and valid-range lessons first. Predict offsets before
running; numeric machine addresses are not fixed expected outputs.

## Offset rules and worked trace

`arr1` owns twenty live integers, initialized to their indexes. `p1` observes
the first one. Adding one to an int pointer advances by one element, whose
storage occupies `sizeof(int)` bytes. It does not advance by one byte. From the
beginning, offsets zero through nineteen name elements. Offset twenty is the
one-past pointer, allowed for a boundary, comparison, or subtraction within this
same array. It must never be dereferenced. Offsets before zero or beyond twenty
must not even be formed. Subtract pointers only within this array and lifetime.

The program first reads zero, then reads index four by both `*(p1 + 4)` and
`arr1[4]`. Prefix increment moves p1 from offset zero to one before dereference,
so the next two reads are one. The current offset is obtained by `p1 - arr1`.
The end pointer is formed from `arr1 + 20`, not from an already advanced pointer.
The traversal checks `cursor != end` before access and reads zero through
nineteen. Its final increment reaches one-past and the next comparison stops.

The original invalid expressions are retained in a disabled comment. After
advancing p1 once, `p1 + 21` attempts offset twenty-two, already outside the
permitted arithmetic range. Independently, `arr1[21]` attempts an invalid element.
A crash is not required for either expression to be wrong. Keep both disabled
in ordinary and diagnostic runs; the safe trace demonstrates their correction.

For a function receiving a raw pointer, the caller must prove actual capacity,
initialization, and lifetime. An explicit size is still necessary. For zero
logical length and a null pointer, return without forming even `pointer + 0`.
Within a nonempty valid range, check an offset before forming its address.

## Learner work and instructor walkthrough

1. Draw twenty numbered elements plus a one-past marker. Predict every read and
   pointer position in the program before execution.
2. Explain why `*(arr1 + i)` and `arr1[i]` agree for a valid element index.
3. Trace the increment, then compute the attempted offset of each disabled
   expression. Identify pointer formation separately from dereference.
4. Replace the trace's valid index four with nineteen and compare the result.
   Explain index twenty and index minus one on paper without executing them.
5. State what an empty range, an unrelated pointer subtraction, and a dangling
   observer violate. Transfer the boundary reasoning into Array Practice.

An instructor can give hints about the owner, current offset, and stopping
comparison while the learner owns the prediction and validity explanation.

## Native workflow and completion evidence

Open the lesson with **Open in IDE**, confirm its import, save the offset table,
and export the ZIP. The browser edits C++; compile the extracted pack natively:

```sh
make main main-debug
./main
ASAN_OPTIONS=detect_leaks=0 ./main-debug
make clean
```

The important reads are zero, four, four, one, and one; the one-past offset is
twenty and traversal reads exactly twenty values. Both builds must be strict
C++20 and both runs sanitizer-clean. Submit the diagram, offset trace, disabled
failure explanations, and changed-index check. From the source repository root,
`python3 verify-array-projects.py` verifies the scoped lesson/project workflows.
