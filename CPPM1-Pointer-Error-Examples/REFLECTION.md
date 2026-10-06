# Reference reasoning

Open this after an attempt. The seven corrections in `repairedExamples()` show:

1. Read and write while the allocation is alive; delete through the sole owner
   once. No observer may dereference after deletion. Clearing both local names
   does not repair unknown aliases elsewhere.
2. Handle absence without dereferencing. A null check covers this state only.
3. Each declarator needs its own `*`; the two corrected pointers alias `value`.
4. Initialize the pointer with the address of a live, initialized object.
5. `*initialized = 5` changes the integer; `initialized = 5` is ill-typed.
6. Initialize `target` itself before reading it. Taking its address is not enough.
7. A string observer has a string pointed-to type, with const preventing mutation.

The ordinary output is 20, an absence message, alias equality 1, 10, 5, 7,
and potatoes, with labels identifying each example. Addresses are not fixed.
The uninitialized-pointer and uninitialized-integer examples have undefined
behavior in this C++20 exercise. Mixed declarators alone are legal, but the
second variable has type int; treating it as a pointer is a type error.

The diagnostic flags intentionally make a null store or a store after deletion.
The earliest invalid operation is the dereference/store, not declaration of an
absent pointer or deletion of a live allocation. Keep these separate from the
corrected ordinary run. Undefined behavior has no required output or crash.
