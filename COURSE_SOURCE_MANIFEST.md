# Course Source Manifest

Canonical source repository: `CPP-Level-2`

## Mapped Catalog Courses

- `cpp-level-2`: C++ Level 2

## Verification Gate

- Run `./verify-course-source.sh` from this repository root before treating the source pack as ready.
- The verification gate checks for this manifest, the source backlog ledger, source-like files, removed Replit metadata, and any repo-specific readiness files.
- Project-specific unit tests or build commands should still be run inside individual project folders when a project includes its own test harness.

## Available source pack folders

The list is an availability inventory, not a readiness certificate for every
pack or proof of every live catalog link. New CPPM3 starter/catalog integration
is delivered separately from the source checks.

| Folder |
| --- |
| `CPPM0-Lifetime-Tracing-Warm-Up` |
| `CPPM0-Ownership-Boundary-Debugging` |
| `CPPM1-Pointer-Error-Examples` |
| `CPPM1-Pointer-Error-Examples-Starter` |
| `CPPM1-Pointer-Practice` |
| `CPPM1-Pointer-Practice-Starter` |
| `CPPM1-Pointers` |
| `CPPM1-Pointers-Starter` |
| `CPPM2-Array-Basics-Reference` |
| `CPPM2-Array-Practice` |
| `CPPM2-Array-Practice-Starter` |
| `CPPM2-Pointer-Arithmetic-Reference` |
| `CPPM2-Tic-Tac-Toe` |
| `CPPM2-Tic-Tac-Toe-Starter` |
| `CPPM3-2D-Array-Extension` |
| `CPPM3-2D-Array-Extension-Starter` |
| `CPPM3-2D-Array-Practice` |
| `CPPM3-2D-Array-Practice-Starter` |
| `CPPM3-Bank-Transactions` |
| `CPPM3-Bank-Transactions-Starter` |
| `CPPM3-Two-Dimensional-Arrays-Reference` |
| `CPPM4-Assembly-Line` |
| `CPPM4-Dynamic-Array-Implementation` |
| `CPPM4-Dynamic-Variables-Reference` |
| `CPPM4-Grocery-List` |
| `CPPM5-Matrix-Fun-with-Matrix-Class` |
| `CPPM5-Modern-Ownership-Reflection` |
| `CPPM5-Profile-Posts` |

## Source Inventory

- Top-level source pack folders: 28
- Source-like files: 84

## Scoped source review

`CPPM1-Pointers` now has a warning-clean C++20 observation reference and a
complete native-workflow brief. Its paired original question starter is
unchanged. Strict compilation, address/value traces, both Make targets and
sanitizer checks cover that one lesson; the inventory gate alone does not
certify every linked project or the broader course audit.

Both CPPM0 projects now have full briefs and separate nested learner/reference
packs. The lifetime starter is a runnable prediction exercise; the ownership
starter requires selection logic. Original parent files remain references.
Run `python3 verify-lifetime-projects.py` for their scoped Make/CMake workflows,
selection edge cases, address/value traces and sanitizers. This does not
certify the remaining manual-memory projects.

The seven CPPM3 packs now have full briefs and independent C++20 Make/CMake
workflows. Required 2D Array Practice and optional Bank Transactions have
separate unfinished starter folders. Run `python3 verify-2d-array-projects.py`
for rectangular-grid, fractional-average, integer-limit, partial-allocation,
ledger-input and mutation checks. Typed nested-row boundaries and genuine flat
storage are distinct. These scoped checks do not certify CPPM4–CPPM5 packs or
the matching catalog/browser delivery.

The optional extension has separate learner/reference packs for checked cell
access and column averages, covered by the same scoped native gate.
