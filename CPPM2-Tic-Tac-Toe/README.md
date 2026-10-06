# Tic Tac Toe with a Flat Raw Array

## Purpose and project role

This optional CPPM2 integration project follows completed Array Practice. Use a
flat array to model nine board cells, validate a move, preserve the current turn
on rejection, and detect a completed game. It extends fixed-storage reasoning
into a stateful console program; it is not another required array exercise.

The learner pack is `CPPM2-Tic-Tac-Toe-Starter`; the reference pack is
`CPPM2-Tic-Tac-Toe`. Both have one main.cpp, a strict C++20 Makefile, and this
complete brief. Three learner bodies remain unfinished: `applyMove`, the
original `checkwin`, and the original `board`. The untouched learner reports
pending tasks and exits; it is not a completed game. The reference's separate
REFLECTION.md discusses the solution after an attempt.

## Board, owner, and state contract

Keep the original global `char square[10]` model. Index zero is an unused marker;
indexes one through nine are live board cells. The digits '1' through '9' mark
empty cells. A placed cell contains X or O. The array owns storage for the
program's lifetime, and no helper owns or retains another allocation. Map cells:

```text
1 | 2 | 3
4 | 5 | 6
7 | 8 | 9
```

Player 1 places X first; Player 2 places O next. The provided driver chooses the
current player's mark and changes players only after a valid, nonterminal move.
The helper's caller supplies the expected current mark on a valid reachable
board. Do not manually alter a completed board to keep playing.

`bool applyMove(int choice, char mark)` returns false for a choice outside 1-9,
a mark other than X/O, an occupied cell, or an already completed board. Rejection
changes no cell. Check the numeric range before indexing. On acceptance, change
exactly the selected cell and return true. The current turn's mark comes from
the driver; this helper does not independently choose a player.

`int checkwin()` observes the board without mutation. Return 1 for any of the
three rows, three columns, or two diagonals containing a winning mark; return
0 for a full board with no win; otherwise return -1. Check a win before a draw.
`void board()` displays the nine cells in their grid and identifies both players.
It observes the state and must not erase, advance, or otherwise alter it.

## Input and ending contract

The provided parser accepts exactly one digit 1-9 after surrounding ASCII
whitespace is removed. Blank input, text, multi-digit input, signs, decimal input,
and trailing tokens are rejected as a whole line. A rejected line or occupied
cell keeps the same player's turn. The input parser is supplied so the project
can focus on board bounds and state.

End-of-input exits once, with an interrupted-game message and no invented result.
A read error reports failure. A win or draw prints its result and exits immediately;
there is no extra Enter-key pause or attempt to process later moves. The program
does not silently reset a completed game. Start a new process for a new board.

## Learner work and instructor walkthrough

1. Draw all ten slots, label index zero as unused, and state the valid move range
   before writing an access. Implement board display and predict the empty grid.
2. Implement applyMove. Test range rejection, occupied cells, invalid marks,
   single-cell mutation, and terminal-board rejection before adding game play.
3. Implement checkwin using the eight winning lines. Predict a row, a column,
   a diagonal, a nearly-winning board, and a full draw. Keep board state unchanged.
4. Play a legal sequence and trace player, chosen cell, acceptance, new board,
   status, and next player after each line. Add invalid input between valid moves.
5. End input before a result and prove the program exits once. Complete a win
   and a draw and prove it does not ask for another move or pause for Enter.

An instructor follows prediction, board diagram, attempted helper, execution,
changed-case check, and explanation. Give staged hints about the valid slot,
current mark, or winning line while the learner owns the implementation.

## Acceptance cases

- All eight winning lines work for either player on reachable boards.
- Full draws and still-playable boards return their distinct status codes.
- Choices zero, ten, negative numbers, occupied cells, and invalid marks are
  rejected without mutation. Whole-line malformed input retains the player.
- A valid move changes one cell, keeps the unused marker, and advances the turn
  only while the game is still playable. A terminal board accepts no new move.
- Empty input and a valid first move followed by end-of-input terminate cleanly.
- One legal win sequence is 1, 4, 2, 5, 3. One draw sequence is
  1, 2, 3, 5, 4, 6, 8, 7, 9. Predict both before checking the reference.

## Native workflow and completion evidence

Open the learner pack with **Open in IDE** and confirm the import. Save the
attempt and export a ZIP. The browser edits C++; compile the extracted pack
with a native C++20 compiler. The untouched starter only reports unfinished work.
After completing the three bodies, run:

```sh
make main main-debug
printf '%s\n' 1 4 2 5 3 | ./main
printf '%s\n' 1 2 3 5 4 6 8 7 9 | ./main
ASAN_OPTIONS=detect_leaks=0 ./main-debug
make clean
```

Both builds must be warning-clean and runs sanitizer-clean. End interactive
input with the platform's end-of-input action. From the source repository root,
`python3 verify-tictactoe-project.py` checks the learner/reference Make/CMake
workflows, completed learner fixture, whole-line input and EOF behavior, and
reachable board states against an independent bit-mask classifier. It does not
certify the remaining CPPM3-CPPM5 projects.

Submit the three helpers, board/range diagram, turn trace, winning-line and draw
cases, invalid/occupied/terminal rejection evidence, and clean EOF evidence.
Keep earlier saved work; a separate current-pack import is offered in the catalog.
