Pseudocode for part 2
```
set of {known_index_values}
dictionary of {filenames:record count starting at 0} (keys predetermined since you already know filenames)

open all of the 52 files (2 unknown, 2 hopped, 48 index)  
open the 4 files (r1, r2, r3, r4) # r2 and r3 contain the indexes
  loop: iterate per record(every 4 lines) in each file
    checking if r2 value & reverseComplement(r3 value) exist in the index set (+checking for Ns):
      no:
        add record w/ adjusted header to unknown files (which depends on if biological R1 or R2)
        increment count of dictionary for the filenames
        # adjusted meaning new header = "{old header}_{r2 value}-{reverseComplement(r3 value)}"
      yes:
        checking if avg quality scores of index read within cutoff:
            no:
                  add record w/ adjusted header to unknown files (which depends on if biological R1 or R2)
                  increment count of dictionary for the filenames
            yes:
              checking if r2 value & reverseComplement(r3 value) match:
                no:
                    add record w/ adjusted header to hopped files(which depends on if biological R1 or R2)
                    increment count of dictionary for the filenames
                yes:
                    add record w/ adjusted header to matched files(which depends on index, and if biological R1 or R2)
                    increment count of dictionary for the filenames
all files closed
return counts for each file for user using the dictionary (how many records added to hopped, unknown, each of the indexes)
```

