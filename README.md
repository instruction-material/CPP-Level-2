# C++ Level 2

This repo now holds the lower-level follow-on course that used to be mixed into
`CPP-Level-1`.

Core flow:
- `CPPM0` lifetime, references, and ownership framing
- `CPPM1` pointers and memory addresses
- `CPPM2` raw arrays and pointer arithmetic
- `CPPM3` two-dimensional arrays and array layout
- `CPPM4` dynamic memory and custom dynamic arrays
- `CPPM5` manual-memory capstones

Scope notes:
- This course assumes students already completed the foundations path in
  `instruction-material/CPP-Level-1`.
- The goal here is explicit reasoning about addresses, layout, ownership,
  resizing, and lifetime.
- The projects intentionally expose raw arrays, `new`/`delete`, and custom
  container mechanics that were removed from the Level 1 path.

Cleanup rules applied here:
- generated binaries such as `main`
- macOS debug bundles such as `*.dSYM`
- local IDE folders such as `.idea/`
- local CMake build trees such as `cmake-build-debug/`
