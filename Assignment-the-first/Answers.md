# Assignment the First

## Part 1
1. Be sure to upload your Python script.

| File name | label | Read length | Phred encoding |
|---|---|---|---|
| 1294_S1_L008_R1_001.fastq.gz | read1 | 101 | Phred+33 |
| 1294_S1_L008_R2_001.fastq.gz | index1 | 8 | Phred+33 |
| 1294_S1_L008_R3_001.fastq.gz | index2 | 8 | Phred+33 |
| 1294_S1_L008_R4_001.fastq.gz | read2 | 101 | Phred+33 |

2. Per-base NT distribution
    1. Use markdown to insert your 4 histograms here.
    
        *Ignore the titles of the histograms, the code is fixed but I don't have time to rerun.
        - index 1
        ![hist_index1](https://user-images.githubusercontent.com/81830809/181865679-21f7f955-8b62-4f89-9266-48dfbe4e6b41.png)
        - index 2
        ![hist_index2](https://user-images.githubusercontent.com/81830809/181865715-7b45a4d7-7646-4ff1-9692-b32ab589ca08.png)
        - biological read 1
        ![hist_read1](https://user-images.githubusercontent.com/81830809/181865721-c3e5b2f3-b6cd-4e91-8271-0b9aa2bc805f.png)
        - biological read 2
        ![hist_read2](https://user-images.githubusercontent.com/81830809/181865733-c3f85031-5bb6-4c44-bc5b-ac30dd3b36ee.png)
    2. What is a good quality score cutoff for index reads and biological read pairs to utilize for sample identification and downstream analysis, respectively? Justify your answer.
        - I determined that a good quality score cutoff for average index reads would be Q20. Q20 would enable the   
    4. How many indexes have undetermined (N) base calls? (Utilize your command line tool knowledge. Submit the command(s) you used. CHALLENGE: use a one-line command)

    
## Part 2
1. Define the problem
    - We need to go through each of the four read files and assemble into two separate groupings (read1+index1, read2+index2). Each of the input files' records belongs to the same cluster, but we need to attach the index read to its corresponding biological read. But, we also need to check for index hopping, index quality score, if the indexes are in our known indexes (and the reverse complement of the index if its from index read 2), etc. (not necessarily in this order). Depending on the results of the conditions we must check for, we need to write them out to files corresponding to their condition(hopped, unknown) and which biological read. Additionally, dual-matched reads need to be written to files depending on their index and which biological read.  

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
8. High level functions. For each function, be sure to include:
    1. Description/doc string
    2. Function headers (name and parameters)
    3. Test examples for individual functions
    4. Return statement
    ```
    def reverseComplement(string -> str) -> str:
        """ 
        Takes a DNA/RNA string as input and returns its reverse complement as a string.
        Usage examples:
            reverseComplement("AATTCCGG")
            -> returns: "CCGGAATT"
            reverseComplement("ATGCATC")
            -> returns: "GATGCAT"
        """
        <code>
        return revComp 
    ```
    Rest of my high level functions are from bioinfo.py.
