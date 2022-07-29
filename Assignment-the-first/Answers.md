# Assignment the First

## Part 1
1. Be sure to upload your Python script.

| File name | label | Read length | Phred encoding |
|---|---|---|---|
| 1294_S1_L008_R1_001.fastq.gz | read1 | 102 | Phred+33 |
| 1294_S1_L008_R2_001.fastq.gz | index1 | 9 | Phred+33 |
| 1294_S1_L008_R3_001.fastq.gz | index2 | 9 | Phred+33 |
| 1294_S1_L008_R4_001.fastq.gz | read2 | 102 | Phred+33 |

2. Per-base NT distribution
    1. Use markdown to insert your 4 histograms here.
    
## Part 2
1. Define the problem
    - We need to go through each of the four read files and assembled into two separate records. .. These records will then be   

3. Describe output
    - Output should be written between 52 total files: 2 different unknowns, 2 different hopped, and 2 different for each of the 24 indexes. 
    - What should it look like? For example, looking at a hopped cluster:
        - going to hopped_R1.fq... new header adds the index from index1 and the reverse-complemented index from index2 
          ```
          @seq_AA-CC
          {sequence line from biological read 1}
          +
          {quality score line from biological read 1}
          ```
        - going to hopped_R2.fq... new header adds the index from index1 and the reverse-complemented index from index2 
          ```
          @seq_AA-CC
          {sequence line from biological read 2}
          +
          {quality score line from biological read 1}
          ``` 
5. Upload your [4 input FASTQ files](../TEST-input_FASTQ) and your [>=6 expected output FASTQ files](../TEST-output_FASTQ).
6. Pseudocode
    ```
    dictionary of {known_index_values:revcomp(known_index_values)}

    open the 4 files (r1, r2, r3, r4) # r2 and r3 contain the indexes
      loop: iterate per record(every 4 lines) in each file
        checking if r2 value & revcomp(r3 value) in the index dictionary:
          no:
            add record w/ adjusted header to unknown
            # adjusted meaning new header = "{old header}_{r2 value}-{revcomp(r3 value)}"
          yes:
            checking if quality scores of index read within cutoff:
                no:
                      add record w/ adjusted header to unknown    
                yes:
                  checking if r2 value & revcomp(r3 value) match:
                    no:
                        add record w/ adjusted header to hopped
                    yes:
                      add record w/ adjusted header to matched
    ```
8. High level functions. For each function, be sure to include:
    1. Description/doc string
    2. Function headers (name and parameters)
    3. Test examples for individual functions
    4. Return statement
