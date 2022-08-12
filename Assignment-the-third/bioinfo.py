#!/usr/bin/env python

# Author: <Kaetlyn Gibson> <kaetlyng@uoregon.edu>

# Check out some Python module resources:
#   - https://docs.python.org/3/tutorial/modules.html
#   - https://python101.pythonlibrary.org/chapter36_creating_modules_and_packages.html
#   - and many more: https://www.google.com/search?q=how+to+write+a+python+module

'''This module is a collection of useful bioinformatics functions
written during the Bioinformatics and Genomics Program coursework.
You should update this docstring to reflect what you would like it to say'''

__version__ = "0.6"         # Read way more about versioning here:
                            # https://en.wikipedia.org/wiki/Software_versioning

DNA_bases = "ATGCN"
RNA_bases = "AUGCN"

def convert_phred(letter: str) -> int:
    """Converts a single character into a phred score"""
    return ord(letter) - 33

def qual_score(phred_score: str) -> float:
    """
    Iterates through an original, unmodified phred score 
    (given as a parameter). Calculates a running total of 
    phred scores. Divides the phred score total by the 
    number of phred scores to get the average quality score.
    """
    total = 0
    totalNumOfScores = len(phred_score)
    for score in range(totalNumOfScores):
        value = convert_phred(phred_score[score])
        total += value
    avg = total/totalNumOfScores
    return avg

def validate_base_seq(seq: str,RNAflag=False) -> bool:
    """
    This function takes a string. Returns True if 
    string is composed of only As, Ts (or Us if RNAflag),
    Gs, Cs, or Ns (unknown base). False otherwise. Case insensitive.
    """
    seq = seq.upper()
    return len(seq) == seq.count("N") + seq.count("A") + seq.count("U" if RNAflag else "T") + seq.count("G") + seq.count("C")

def gc_content(DNA: str) -> float:
    """
    Returns GC content of a DNA sequence as a decimal 
    between 0 and 1.
    """
    # check if sequence is DNA
    if validate_base_seq(DNA, False):
        DNA = DNA.upper()         
        Gs = DNA.count("G")     
        Cs = DNA.count("C")    
        return (Gs+Cs)/len(DNA)
    else:
        return "Not a DNA sequence."

def oneline_fasta(fastafile: str) -> None:
    """
    Takes in a string for a file name as input. Opens a fasta file
    and writes out to a new "temporary" file with each fasta record
    on one line. No return.
    """
    outFile = open(fastaFile + "_temp.fa", "w")
    with open(fastaFile, "r") as faFile:
        seq = ""
        for i, line in enumerate(faFile):
            if ">" in line[0]:
                line = line.replace("\n", " ")
                # if 1st record, write it out
                # otherwise, need to write out seq then
                # reset seq for the next record
                if i > 1:
                    outFile.write(seq)
                    outFile.write("\n")
                    seq = ""
                outFile.write(line)
            else:
                line = line.strip()
                seq += line
        outFile.write(seq)
    outFile.close()
    return None

def reverse_complement(string:str) -> str:
    """Given a string, returns the reverse complement of the string."""
    swapDict = {"A":"T", "T":"A", "G":"C", "C":"G", "N":"N"}
    revComp = ""
    for char in string:
        revComp += swapDict[char]
    revComp = revComp[::-1]
    return revComp

if __name__ == "__main__":
    # Check that convert_phred returns the correct value for several different inputs
    assert convert_phred("I") == 40, "wrong phred score for 'I'"
    assert convert_phred("C") == 34, "wrong phred score for 'C'"
    assert convert_phred("2") == 17, "wrong phred score for '2'"
    assert convert_phred("@") == 31, "wrong phred score for '@'"
    assert convert_phred("$") == 3, "wrong phred score for '$'"
    # Check that qual_score returns the correct avg value for multiple inputs 
    assert qual_score("BBBBBBBB####################################################") == 6.133333333333334, "wrong average score for given quality score line"
    assert qual_score("=AA@AAAAAAAA&@20000/@=A@####################################") == 11.666666666666666, "wrong average score for given quality score line"
    # Check that validate_base_seq correctly identifies strings as DNA, RNA, or neither 
    assert validate_base_seq("AATAGAT", False) == True, "Validate base seq does not work on DNA"
    assert validate_base_seq("AAUAGAU", True) == True, "Validate base seq does not work on RNA"
    assert validate_base_seq("AATAGAT") == True, "Default is RNAflag set to False, this is DNA."
    assert validate_base_seq("TATUC", False) == False, "Checking for U's"
    assert validate_base_seq("UCUGCU", False) == False, "Checking for U's"
    assert validate_base_seq("UCUGCUB") == False, "Does not catch neither cases"
    # Check that gc_content returns the correct values (decimal between 0 and 1)
    assert gc_content("GCGCGC") == 1 
    assert gc_content("AATTATA") == 0
    assert gc_content("GCATGCAT") == 0.5
    assert gc_content("GCATGCATU") == "Not a DNA sequence."
    # No test case for oneline_fasta in this version!
    # Check that reverse_complement returns the correct string
    assert reverse_complement("GTAGCGTA") == "TACGCTAC", "wrong reverse complemet"
    assert reverse_complement("CGATCGAT") == "ATCGATCG", "wrong reverse complemet"
    assert reverse_complement("GATCAAGN") == "NCTTGATC", "wrong reverse complemet"
