#!/usr/bin/env python

import argparse
import bioinfo
import gzip
import numpy as np
import matplotlib.pyplot as plt

# global variable flags
def get_args():
    parser = argparse.ArgumentParser(description="A program for understanding mean Qscores")
    parser.add_argument("-f", "--infile", help="Specify the input file name.", type=str, required=True)
    parser.add_argument("-o", "--outimg", help="Specify the output image name.", type=str, required=True)
    parser.add_argument("-p", "--positions", help="Specify the number of base pair positions (readlength).", type=int, required=True)
    parser.add_argument("-r", "--records", help="Specify the number of records.", type=int, required=True)
    return parser.parse_args()	
args = get_args()

# initialize array
mean = np.zeros((args.positions), dtype=float)
# open the file
with gzip.open(args.infile,"rt") as faFile:
    i = 0
    for line in faFile:
        line = line.strip()
        i += 1
        if i % 4 == 0:
            qualityLine = line.strip()
            for basepos, letter in enumerate(qualityLine):
                score = bioinfo.convert_phred(letter)
                mean[basepos] += score                              
for basepos in range(args.positions):
    mean[basepos] = mean[basepos]/args.records

# Plotting
plt.style.use("seaborn-whitegrid")
plt.bar(np.arange(args.positions), mean, color="r")
plt.xlabel("Nucleotide Position") 
plt.ylabel("Mean QScore")
plt.title("Per Nucleotide Mean Distribution")
plt.savefig(args.outimg) 