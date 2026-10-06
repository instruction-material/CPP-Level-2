# Bank Transactions

Use `CPPM3-Bank-Transactions-Starter` for an attempt. The named
`CPPM3-Bank-Transactions` pack is the completed reference; `REFLECTION.md`
follows the attempt. This is an optional
applied grid after required 2D Array Practice, using fictional names and whole
integer units. It is a programming model, with no real account connection.

## Original model and purpose

Keep the original built-in `int balances[4][5]`, one initial row and exactly
three transaction rows. The five columns are transaction number, MMDDYYYY date,
opening balance, signed amount, and ending balance. The initial row is number
zero, has amount zero, and has equal opening/ending balances. A transaction's
opening balance is the preceding completed row's ending balance. Positive
amounts are deposits and negative amounts are withdrawals; negative balances
remain allowed by this exercise.

The purpose is to defend column meanings and partial-state boundaries in a
realistic input flow. Use typed `int (*)[5]` row traversal through the array
parameter, not `*balances` passed as a flat pointer. The caller establishes
four rows of initialized, live storage and calls row writers in order.

## Three learner tasks

1. `initializeLedger` validates the provided date and detectable null input,
   writes the five initial-row cells, returns true, and preserves other rows.
   Invalid input returns false before any mutation. Calendar validation is
   supplied; this task is about the row schema.
2. `recordTransaction` accepts only transaction numbers 1–3, a valid date,
   and nonnull storage. The preceding row must already be initialized by the
   caller. Check whether adding the signed amount would exceed `INT_MIN` or
   `INT_MAX` before addition. Reject any invalid/unrepresentable request with
   false and preserve every cell. On success write exactly the selected row
   from its number, date, prior ending balance, amount and new ending balance.
3. `print` reads only the requested initialized row prefix. Reject negative
   or more-than-four rows, a column count other than five, and null-positive
   rows with `std::invalid_argument` before access. Null plus zero rows prints
   nothing. Use the original five labels, preserve input, and display a date
   with eight digits, including a leading zero where necessary.

Provided readiness checks report unfinished task bodies before prompting.
The input driver, ASCII trimming, whole-number parser and calendar helper are
complete scaffolding; keep the three row tasks as the learner work.

## Input and partial-state behavior

The fictional name can include spaces and must be nonempty after trimming.
Balances and amounts accept a single whole integer, with an optional sign and
ASCII surrounding whitespace, within the `int` range. Fractional numbers,
trailing text, extra tokens and out-of-range integers are rejected and retried.
Dates require exactly eight digits after trimming and a valid Gregorian date
with year 0001–9999. Rejected dates or numbers leave the ledger unchanged.
The original MMDDYYYY integer representation is retained; the printer restores
its leading zero. A transaction date need not be later than earlier dates.

An amount that would overflow the balance is retried for the same transaction.
Only a completed, accepted transaction advances the row count. End-of-input
exits once with status zero and prints only the completed rows; a stream read
error reports failure with status one. If input ends before the initial row is
complete, there is no ledger prefix to print. No uninitialized row is printed.

## Walkthrough, hints and acceptance

Draw the four-by-five schema and predict a deposit, withdrawal and unchanged
balance. Attempt one task, run it, then trace the prior-ending to next-opening
link. An instructor can first identify a column, next identify the committed
row count, then ask which checks must happen before a write. Keep reference
reflection until after the attempt.

| Case | Required result |
| --- | --- |
| Starting 100; amounts 20, -30, 0 | Ending balances 120, 90, 90 in three accepted rows |
| A name with spaces | Full fictional name retained |
| January 1 date `01012025` | Eight-digit printed date |
| Leap/non-leap February and impossible month/day | Valid dates accepted, invalid dates retried |
| Fraction, extra token, junk, blank or out-of-range number | Retry without committing a row |
| `INT_MAX` plus 1, or `INT_MIN` minus 1 | Reject before addition and mutation |
| End-of-input during any field | Exit once; print only the initialized prefix |
| Null, wrong column count or invalid row/index count | Reject before access |

## Native workflow

The site IDE edits, saves, reopens, and exports C++. Compilation uses a native
C++20 compiler. Select **Start in IDE**, confirm the import, save an attempt,
export a ZIP, extract it, and run:

```sh
make main main-debug
./main
ASAN_OPTIONS=detect_leaks=0 ./main-debug
make clean
```

Both builds must be warning-clean and diagnostic runs must have no sanitizer
report. Leak detection is disabled for platforms without LeakSanitizer support;
this command alone does not prove that every allocation was released. The
scoped gate separately tracks table allocation failures and cleanup.

From the source repository root, run `python3 verify-2d-array-projects.py`.
The untouched learner reports its pending tasks and exits safely. Complete the
task bodies before treating its successful exit as exercise completion. Use the
course's current-pack link to keep an earlier saved project and import the
current files into a different project key.

## Completion evidence

Submit the three task bodies, labeled schema, three-row balance trace,
overflow-before-write explanation, input fixtures and EOF-at-each-field checks.
Show that rejected updates and printing preserve all cells. Include warning-
clean builds and sanitizer-clean runs. This optional choice adds an input and
transaction-state model; the required practice already supplies grid statistics.
