# CPPM0 Project 2: Ownership Boundary Debugging

Use a small record-processing program to identify copies, mutating references,
read-only references, and borrowed observations.

Practice goals:
- label which function owns each object
- explain which calls mutate caller-owned data
- avoid returning observations to objects that no longer exist
- use addresses and output traces to prove the data flow

Student extension:
- add one more function that should not be allowed to mutate the caller's data,
  then enforce that with a `const` reference.
