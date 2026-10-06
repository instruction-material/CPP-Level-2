# Reference reflection after an attempt

The original four-by-five nested array retains its row type at the printer's
boundary. Each transaction checks its index, date and representability before
writing a complete row. The input driver retries the same field/transaction on
rejection and advances the initialized row prefix only after success. EOF can
print that prefix without inventing an incomplete transaction. No cast or
pointer stride across an int subarray is needed. Trace a rejection at each
field and show that the previously completed rows remain byte-for-byte intact.
