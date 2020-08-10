# 0.1.0

## Added

- add check to catch errors with using multiple strings specs in Key,Text,Mouse action,e.g. `Key("c-a","c-c")` vs `Key("c-a,c-c")`

- add checks so that `BringApp`,`StartApp` do not use dyn-strings and suggest refactoring

## Changed

- The checks for mimic can now generate an error messages dynamically allowing to show precise suggestions on how to correct them!

