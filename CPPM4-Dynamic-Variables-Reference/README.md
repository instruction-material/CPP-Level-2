# Dynamic variables: a worked lifetime reference

This supplied, complete C++20 lesson supports independent reading or a shared
walkthrough. It preserves the original integer and string pointer examples.
There are no unfinished project tasks in this pack.

A pointer is a variable containing an address. `new int{value}` creates and
initializes an unnamed integer object whose lifetime extends until deletion;
the local pointer variable and that object have separate lifetimes. `*p1` reads
the object only while it is live. A successful allocation needs one owner and
exactly one cleanup path, even if an operation throws.

`delete p1` destroys the object and releases its storage. It does not set the
pointer to null or make the old integer become zero. Dereferencing afterward
uses a dangling pointer and has undefined behavior. Assigning `p1 = nullptr`
marks this particular pointer absent; it does not repair other aliases or
restore the deleted object. This program never dereferences deleted storage.

## Read and run

The pack contains `main.cpp`, `Makefile` and this README. With a native C++20
compiler and Make, run `make`, then `./main`. Enter one complete decimal integer,
for example `5`. Leading/trailing whitespace and one optional sign are allowed;
the value must fit the platform's `int`. Blank lines, fractions, trailing text
and out-of-range values are rejected with status 1 before object allocation.
EOF before a line ends cleanly with status 0. A failed read returns status 1.

For input `5`, the observable trace includes:

```text
The value of *p1 is: 5
Cleaning up p1.
After deletion, p1 is nullptr: true
String pointer lifecycle
Dynamic input
Live string address: <an address that may change between runs>
After deletion, strPtr is nullptr: true
```

Trace each successful `new`, live dereference, `delete` and null assignment in
the supplied code. The catch paths delete the owned object before propagating
an output exception; allocation failure never creates an object to delete.
The string is initialized during construction, follows the same ownership
sequence, and is destroyed with scalar `delete`, not `delete[]`.

Run `make main-debug` and `./main-debug` with the same input for AddressSanitizer
and UndefinedBehaviorSanitizer checks. A normal reference run must complete
without either diagnostic. `make clean` removes both programs and macOS debug
bundles. The scoped repository gate is `python3 verify-dynamic-lifetime.py`.

## Explain the boundaries

Before proceeding to the custom-array project, draw the pointer variable and
the live heap object separately. Explain why the address is not the value, why
a dangling alias must not be dereferenced, why null assignment cannot fix a
leak, and how an exception follows its cleanup path. Compare this manual lab
with a stack value or `std::unique_ptr`, which supplies automatic cleanup in
ordinary production code. Keep scalar `delete` and array `delete[]` distinct.
