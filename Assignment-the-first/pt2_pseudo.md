Pseudocode for part 2
```
dictionary of known_index_values:revcomp(known_index_values)
open the 4 files (r1, r2, r3, r4) # r2 and r3 contain the indexes
  loop: record of each file
    checking if r2 value & revcomp(r3 value) in the index dictionary:
      yes:
        checking if quality scores within cutoff:
            yes:
              checking if r2 value & revcomp(r3 value) match:
                yes:
                  add to matched
                no:
                  add to hopped
            no:
              add to unknown
      no:
        add to unknown
```

check cutoff per nucleotide position? or for the whole record? 
  probably for the biological reads?
what is my cutoff?
