# Course Source Manifest

Canonical source repository: `CPP-Level-2`

## Mapped Catalog Courses

- `cpp-level-2`: C++ Level 2

## Verification Gate

- Run `./verify-course-source.sh` from this repository root before treating the source pack as ready.
- The verification gate checks for this manifest, the source backlog ledger, source-like files, removed Replit metadata, and any repo-specific readiness files.
- Project-specific unit tests or build commands should still be run inside individual project folders when a project includes its own test harness.

## Active Catalog Targets

| Folder |
| --- |
| `CPPM0-Lifetime-Tracing-Warm-Up` |
| `CPPM0-Ownership-Boundary-Debugging` |
| `CPPM1-Pointer-Error-Examples` |
| `CPPM1-Pointer-Practice` |
| `CPPM1-Pointers` |
| `CPPM1-Pointers-Starter` |
| `CPPM2-Array-Basics-Reference` |
| `CPPM2-Array-Practice` |
| `CPPM2-Array-Practice-Starter` |
| `CPPM2-Pointer-Arithmetic-Reference` |
| `CPPM2-Tic-Tac-Toe` |
| `CPPM3-2D-Array-Practice` |
| `CPPM3-Bank-Transactions` |
| `CPPM3-Two-Dimensional-Arrays-Reference` |
| `CPPM4-Assembly-Line` |
| `CPPM4-Dynamic-Array-Implementation` |
| `CPPM4-Dynamic-Variables-Reference` |
| `CPPM4-Grocery-List` |
| `CPPM5-Matrix-Fun-with-Matrix-Class` |
| `CPPM5-Modern-Ownership-Reflection` |
| `CPPM5-Profile-Posts` |

## Source Inventory

- Top-level folders: 21
- Active linked folders: 21
- Ledgered inactive/support folders: 0
- Source-like files: 49

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
