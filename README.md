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

## CPPM1 pointer workflows

The pointer-error challenge and pointer-practice choice each have a separate
`-Starter` folder and a reference folder with the original name. Each import
contains one entry point. Starter runs report unfinished tasks rather than
pretending to be a completed exercise. Their READMEs contain the full contracts,
acceptance cases, instructor walkthrough, and native commands. Error diagnostics
require explicit flags and an AddressSanitizer build; default runs are defined.

Run `python3 verify-pointer-projects.py` from this repository root to verify the
four independent Make workflows, five CMake targets, strict C++20 compilation,
sanitizer-clean normal runs, explicit null/dangling diagnoses, and practice edge
cases. This scoped gate does not certify the remaining CPPM2-CPPM5 projects.

## CPPM2 array workflows

The two worked lessons and the required Array Practice learner/reference packs
have independent strict C++20 Make workflows and full neutral briefs. Practice
retains the four original tasks, sample squares starting at zero, and three
public observer signatures. Empty, invalid, and unrepresentable ranges have
explicit contracts. The arithmetic reference keeps its original invalid
expressions disabled and uses one-past only as a traversal boundary.

Run `python3 verify-array-projects.py` for the four Make workflows, four CMake
targets, completed learner fixtures, logical-prefix and mutation checks,
sanitizer-clean lesson runs, and native array cases. This gate does not certify
Tic Tac Toe or the remaining CPPM3-CPPM5 projects.

## Optional CPPM2 Tic Tac Toe integration

The separate learner and reference packs retain the original flat board and
checkwin/board interfaces. Three task bodies, full input/turn/end-state contracts,
whole-line parsing, clean EOF, and strict native workflows make the integration
project usable without exposing the completed solution as its starter.
Run `python3 verify-tictactoe-project.py` for its scoped native gate.

## CPPM3 shape and input workflows

The worked two-dimensional array lesson distinguishes typed nested rows, a real
flat rectangular array and separately allocated row pointers. Required practice
preserves its four original tasks and sample grid, with a separate unfinished
`CPPM3-2D-Array-Practice-Starter` and double row averages. The optional Bank
Transactions model preserves its four-by-five grid and three transactions,
with a separate `CPPM3-Bank-Transactions-Starter`. Both paired briefs contain
complete contracts, staged hints, self-checks, native commands and ownership or
partial-state evidence. Completed reference reflection remains separate.

Run `python3 verify-2d-array-projects.py` for the seven strict Make workflows,
seven independent CMake targets, completed learner fixtures, rectangular and
integer boundary cases, allocation-failure cleanup, ledger mutation/input/EOF
cases and sanitizer runs. The inventory gate and these scoped checks do not
certify the remaining CPPM4–CPPM5 source, catalog imports or production state.

The optional `CPPM3-2D-Array-Extension-Starter` and matching reference add two
new tasks after practice: checked coordinate access and column averages. They
have their own project identity, full brief and native gate coverage so the
extension challenge has a concrete purpose and matching source material.
