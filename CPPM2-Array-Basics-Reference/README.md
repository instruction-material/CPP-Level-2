# Raw Arrays as Contiguous Memory

## Purpose and prerequisites

This CPPM2 lesson precedes the required Array Practice project. It connects the
Level 1 collection model with fixed storage, initialized elements, explicit
bounds, and ownership lifetime. Read the CPPM0/CPPM1 owner, observer, reference,
and pointer vocabulary first. This reference is a worked lesson to trace with
an instructor or independently, rather than a second unfinished project.

## Read and trace

`int nums[10] = {}` creates ten initialized zero-valued integers. `const int
arr[3] = {1, 2, 3}` creates three initialized integers that cannot be changed
through that array. Their sizes are capacities. Valid element indexes are
`[0, 10)` and `[0, 3)`, respectively. The automatic arrays own their storage
until the enclosing scope ends; pointers and references can observe elements
only within that lifetime.

The program reads `nums[3]`, changes it to 42, and reads it again, then reads
`arr[0]`. Predict those values. In the same scope, `sizeof(nums) / sizeof(nums[0])`
computes capacity because `nums` is still an array object. It does not measure
a logical prefix and does not work as an element count after an array parameter
has decayed to a pointer. Draw ten numbered slots before tracing each loop.

The first loop assigns indexes zero through nine. The second prints those ten
stored values. Both stop before the capacity. A later one-past address may be
used for a traversal boundary, but there is no element at index ten.

## Learner work and instructor walkthrough

1. Predict the initial four output lines and both loops before running.
2. Mark initialized values, writable storage, constant storage, and lifetime
   on a diagram. Explain which statement mutates an element.
3. Explain why a function receiving `int values[]` still needs a size parameter.
   State the valid index range for a logical prefix of length three within ten
   elements. Do not obtain capacity by applying sizeof to the parameter.
4. Change one valid index and compare prediction with output. Classify an index
   outside the range on paper; do not enable an invalid read to find its value.
5. Carry the same explicit range and ownership diagram into Array Practice.

An instructor follows prediction, diagram, execution, changed-case check, and
explanation. Staged hints should identify the array object and its bounds.

## Native workflow and completion evidence

Open the lesson with **Open in IDE**, confirm its import, save a trace, and export
the ZIP. The browser edits C++; it does not compile it. Extract the pack and run:

```sh
make main main-debug
./main
ASAN_OPTIONS=detect_leaks=0 ./main-debug
make clean
```

The output begins `0`, `42`, `1`, `10`, then prints zero through nine on separate
lines. Both builds must be warning-clean C++20 and both runs sanitizer-clean.
Submit the storage diagram, predicted/observed output, logical-prefix range,
and changed-index explanation. The source gate is `python3 verify-array-projects.py`
from the repository root; it certifies these scoped examples only.
