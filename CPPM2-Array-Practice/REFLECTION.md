# Reference reflection

Compare the attempt before reading the reference functions. The ten squares
start at zero, so the first and last values differ and their sum is 285. The
original ASCII words total 17 bytes. Zero logical length has no first or last
object; it must return before access. The caller proves capacity and lifetime,
while the provided check only rejects detectable size/null violations.

The reference checks each integer addition before it happens. Opposite signed
values are allowed when each ordered prefix remains representable. An invalid
prefix is rejected even if later cancellation would make the mathematical total
fit. String sizes are checked against the remaining nonnegative int capacity
before conversion and addition. Unicode byte counts remain byte counts.

Only fillPerfectSquares mutates storage. The other functions borrow and observe
it, returning without retained aliases. Compare a diagram and independent test
expectations with the reference; a successful sanitizer run is evidence for
those inputs, not proof that arbitrary caller-supplied pointers are valid.
