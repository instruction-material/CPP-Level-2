# Pointer observation reference

This is the complete observation program paired with the separate
`CPPM1-Pointers-Starter` questions. Predict the values and alias relationships
before running it; compare with this reference afterward. Compile this one
program, never combine it with another folder's `main.cpp`.

```sh
c++ -std=c++20 -Wall -Wextra -Wpedantic -Werror main.cpp -o pointers
./pointers
```
`make` and `make main-debug` use the same warning-clean C++20 baseline. The site
IDE edits, saves and exports source; use a native compiler to run C++.

`val` starts at 5. `p1` observes its address; `*p1` reads that object's value.
Assigning 10 through `p1` changes both ways of reading `val`. Assigning `p2 = p1`
copies an address, so the two pointers observe the same object. Assigning 20
through `p2` changes what `val` and `*p1` report. The printed non-null addresses
agree within one run, but their spelling and numeric value depend on the build
and run; they are not fixed expected output. No pointer owns or deletes `val`,
whose lifetime covers all these observations.

The uninitialized-pointer discussion stays in comments. In C++20, merely reading
an uninitialized pointer, including printing it, already has undefined behavior.
A crash or compiler error is not guaranteed. The executable `p3` is initialized
to `nullptr`; both it and `p4` may be printed but must not be dereferenced.
Their printed null spelling is implementation-defined. Never enable the unsafe
commented statements as an ordinary test of this reference.

For the final syntax questions, keep assignments to the pointed-to integer
distinct from assignments to the pointer itself. Predict which operand types
are required before writing an expression. Retain the value trace, alias
diagram, compiler command and the lifetime explanation. The unchanged starter
contains the questions without executable reference answers.
