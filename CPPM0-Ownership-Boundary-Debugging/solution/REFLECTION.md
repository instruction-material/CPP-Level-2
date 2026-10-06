# Reference reflection

The first entry starts at 2. Editing a copy prints 7 but leaves the vector entry
at 2; editing by reference makes that entry 7. The third entry, 8, remains the
highest. The strict greater-than comparison preserves the earliest maximum in
a tie. Empty input throws before indexing, one entry returns that same element,
and negative severities compare normally. The returned const reference borrows
an element. Grow or erase first, then reacquire observations; never read through
an invalidated reference. Recompute after changes that can alter the maximum.
