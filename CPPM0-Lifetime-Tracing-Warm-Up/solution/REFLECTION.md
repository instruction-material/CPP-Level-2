# Reference reflection

Taylor's card starts at 70. `updateCopy` prints its own value of 80, leaving the
caller at 70. `updateReference` makes the caller 80; the const observer leaves it
there. The caller, mutating reference and const view refer to the same object;
the value parameter is distinct. Morgan's bonus is 100 and remains valid after
return. Named return value optimization permits the local and result to be the
same object, so an ordinary trace must not promise different addresses.
