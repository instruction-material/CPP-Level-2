# Reference reflection

The flat board retains the original unused index zero and nine numbered cells.
The move helper rejects the range before access and a finished board before
mutation. A valid caller supplies the current player's mark; the driver owns
alternation. Occupied and malformed moves do not change the player or board.

The original eight-line checkwin implementation remains, with win tested before
full-board draw. Board rendering observes all nine cells. Whole-line parsing
prevents partial numeric consumption from becoming a move. EOF ends once rather
than reusing a prior choice with a failed stream. Win and draw end immediately,
so a completed position is preserved rather than reset or advanced.

Compare predictions and attempted helpers with the reference. The native gate
uses an independent bit-mask traversal of reachable states, including terminal
positions, and legal/interrupted input scripts. This evidence does not prove
arbitrarily hand-corrupted boards or external caller turn violations are valid.
