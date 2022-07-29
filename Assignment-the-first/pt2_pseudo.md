Pseudocode for part 2
```
dictionary of {known_index_values:revcomp(known_index_values)}

open the 4 files (r1, r2, r3, r4) # r2 and r3 contain the indexes
  loop: iterate per record(every 4 lines) in each file
    checking if r2 value & revcomp(r3 value) in the index dictionary:
      yes:
        checking if quality scores of index read within cutoff:
            yes:
              checking if r2 value & revcomp(r3 value) match:
                yes:
                  add record w/ adjusted header to matched
                   # adjusted meaning new header = "{old header}_{r2 value}-{revcomp(r3 value)}"
                no:
                  add record w/ adjusted header to hopped
            no:
              add record w/ adjusted header to unknown
      no:
        add record w/ adjusted header to unknown
```

