#!/usr/bin/env python
import argparse
import bioinfo
import gzip

# global variable flags
def get_args():
    parser = argparse.ArgumentParser(description="A program for understanding mean Qscores")
    parser.add_argument("-k", "--known", help="Specify the input known indexes file name.", type=str, required=True)
    parser.add_argument("-r1", "--read1", help="Specify the input read1 file name.", type=str, required=True)
    parser.add_argument("-i1", "--index1", help="Specify the input index1 file name.", type=str, required=True)
    parser.add_argument("-i2", "--index2", help="Specify the input index2 file name.", type=str, required=True)
    parser.add_argument("-r2", "--read2", help="Specify the input read2 file name.", type=str, required=True)
    parser.add_argument("-n", "--numRecords", help="Specify the number of records.", type=int, required=True)
    return parser.parse_args()	
args = get_args()

# higher level functions
def getRecord(file:str) -> list:
    """Obtains and returns a single record from a given fasta file."""
    header = file.readline().strip()
    sequence = file.readline().strip()
    add = file.readline().strip()
    quality = file.readline().strip()
    return [header, sequence, add, quality]

def writeToFile(filename, record, header, i1_index, i2_index) -> None:
    """Writes updated records to two given files depending on the biological read."""
    if filename in outFiles:
        f = outFiles[filename]
        record[0] = header+"_"+i1_index+"-"+i2_index
        for item in range(4):
            f.write(record[item]+"\n")
    return None

# initialize set, dictionaries, and summary variables
knownIndex = set()
outFiles = {'unknown_R1.fq':'', 'unknown_R2.fq':'', 'hopped_R1.fq':'', 'hopped_R2.fq':''}
recordCt = {'unknown_R1.fq':0, 'unknown_R2.fq':0, 'hopped_R1.fq':0, 'hopped_R2.fq':0}
matchedDist, hoppedDist = {}, {}
dualmatchTot, unknownTot, hoppedTot, recTot = 0, 0, 0, 0
# populate set and dictionaries from known index file
indexFile = open(args.known, "r")
for line in indexFile:
    line = line.split("\t")[4].strip()
    if bioinfo.validate_base_seq(line):
        knownIndex.add(line)
        f1 = line + '_R1.fq'
        f2 = line + '_R2.fq'
        outFiles[f1] = ''
        outFiles[f2] = ''
        recordCt[f1] = 0
        recordCt[f2] = 0
# open read files
read1 = gzip.open(args.read1,"rt")
index1 = gzip.open(args.index1,"rt")
index2 = gzip.open(args.index2,"rt")
read2 = gzip.open(args.read2,"rt")
openedFiles = [read1, index1, index2, read2]
for filename in outFiles:
    f = open("./results/"+filename, "w")
    outFiles[filename] = f
    openedFiles.append(f)
# main loop
i = 0
while i < args.numRecords: 
    i += 1
    recTot += 1
    record = {"read1":getRecord(read1), "index1":getRecord(index1), "index2":getRecord(index2), "read2":getRecord(read2)}
    header = record["read1"][0]
    i1_index = record["index1"][1]
    i2_index = bioinfo.reverse_complement(record["index2"][1])
    i1_i2 = i1_index + "_" + i2_index
    # check for N and if the indexes do not exist in our known indexes
    if ((i1_index not in knownIndex)or(i2_index not in knownIndex)):
        # for writing out to file
        writeToFile("unknown_R1.fq", record["read1"], header, i1_index, i2_index)
        writeToFile("unknown_R2.fq", record["read2"], header, i1_index, i2_index)
        # for summary file
        recordCt["unknown_R1.fq"] += 1
        recordCt["unknown_R2.fq"] += 1
        unknownTot += 1
    else:
        # check if mean quality score for the indexes below cutoff of 30
        i1_avgScore = bioinfo.qual_score(record["index1"][3])
        i2_avgScore = bioinfo.qual_score(record["index2"][3])
        if ((i1_avgScore<30)or(i2_avgScore<30)):
            # for writing out to file
            writeToFile("unknown_R1.fq", record["read1"], header, i1_index, i2_index)
            writeToFile("unknown_R2.fq", record["read2"], header, i1_index, i2_index)
            # for summary file
            recordCt["unknown_R1.fq"] += 1
            recordCt["unknown_R2.fq"] += 1
            unknownTot += 1
        else:
            # check if indexes do not match
            if i1_index != i2_index:
                # for writing out to file
                writeToFile("hopped_R1.fq", record["read1"], header, i1_index, i2_index)
                writeToFile("hopped_R2.fq", record["read2"], header, i1_index, i2_index)
                # for summary file
                recordCt["hopped_R1.fq"] += 1
                recordCt["hopped_R2.fq"] += 1
                if (i1_i2) not in hoppedDist:
                    hoppedDist[i1_i2] = 1
                else:
                    hoppedDist[i1_i2] += 1
                hoppedTot += 1
            else:
                # for writing out to file
                writeToFile(i1_index+"_R1.fq", record["read1"], header, i1_index, i2_index)
                writeToFile(i1_index+"_R2.fq", record["read2"], header, i1_index, i2_index)
                # for summary file
                recordCt[i1_index+"_R1.fq"] += 1
                recordCt[i1_index+"_R2.fq"] += 1
                if i1_i2 not in matchedDist:
                    matchedDist[i1_i2] = 1
                else:
                    matchedDist[i1_i2] += 1
                dualmatchTot += 1
# close files
for filename in openedFiles:
    filename.close()

# write out summary of results
with open('summary.txt', 'w') as summary:
    summary.write(f"=================================|SUMMARY|=================================\n")
    summary.write(f"Number of dual-matched index records: {dualmatchTot}, Percent of records: {round((dualmatchTot/recTot)*100, 2)}%\n")
    maxMatchedIndex = max(matchedDist, key=lambda key: matchedDist[key])
    maxMatchedVal = round((matchedDist[maxMatchedIndex]/dualmatchTot)*100, 2)
    summary.write(f"\tMost common matched index pair: {maxMatchedIndex}, Percent of matched: {maxMatchedVal}%\n")
    summary.write(f"Number of unknown index records: {unknownTot}, Percent of records: {round((unknownTot/recTot)*100, 2)}%\n")
    summary.write(f"Number of hopped index records: {hoppedTot}, Percent of records: {round((hoppedTot/recTot)*100, 2)}%\n")
    maxHoppedIndex = max(hoppedDist, key=lambda key: hoppedDist[key])
    maxHoppedVal = round((hoppedDist[maxHoppedIndex]/hoppedTot)*100, 2)
    summary.write(f"\tMost common hopped index pair: {maxHoppedIndex}, Percent of hopped: {maxHoppedVal}%\n")
    summary.write(f"Total number of records: {recTot}\n\n")
    summary.write(f"Number of Records Per file breakdown:\n")
    summary.write(f"File\t\t\tCount\n")
    summary.write("=====================\n")
    for filename in recordCt:
        summary.write(f"{filename}\t{recordCt[filename]}\n")   
    summary.write(f"===========================================================================\n")