# Reference reasoning

Read after attempting the three questions. The fixed source retains the original
sample inputs and scan-all algorithm, with explicit empty and boundary behavior.

Question 1 reads offsets 0..9 and 0,2,..18. The first pointer ends at offset 10;
the second ends one-past-end at 20 and is never dereferenced there. Debug 1a and
1c use the array object as a pointer, which is ill-typed. Correct those initial
addresses before analyzing their loops: pre-increment skips the first element
and dereferences offset 20 on the last two-step iteration. Debug 1b also declares
only its first name as a pointer. The labeled declaration correction now uses
`.data()` and gives both observers pointer types.

Question 2 alternates moves and checks equality after the first move. For an
even length this prevents the pointers crossing without equality. For length n
greater than zero, the forward count is n/2 and backward count is (n-1)/2. The
meeting offset is n/2. Empty input returns before evaluating size minus one or
forming a last-character pointer. The vector owns the storage and is not resized
while it is borrowed. The appended null terminator is not a logical character.

Question 3 scans all characters left to right, with an independent result
offset. A non-digit or zero does not move the result; neither stops scanner
progress. The result remains inside the logical string because each digit is
checked against the remaining length before advancing. A move equal to the
remaining length is rejected, and the entire scan stops. Subtraction avoids an
overflowing offset-plus-increment test. Explicit ASCII comparisons prevent
locale-specific digit classifications from changing the assignment.

`1a2bc` ends at b, offset 3. A jump-only interpretation would stop at a and is a
different exercise. `0a1b` ends at a, offset 1; it does not loop forever on zero.
`4abc1` ends at 1, offset 4 and rejects the final move. `9a1bc` stops on the
first digit with result offset 0. The two implementations agree and do not
modify the borrowed string or keep an observer after the function returns.
