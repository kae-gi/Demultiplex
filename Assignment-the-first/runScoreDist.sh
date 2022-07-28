#!/bin/bash
#SBATCH --account=bgmp
#SBATCH --partition=bgmp
#SBATCH --cpus-per-task=4
#SBATCH --nodes=1
#SBATCH --time=10:00:00
#SBATCH --job-name=scoreDist
#SBATCH --output=scoreDist_%j.out
#SBATCH --error=scoreDist_%j.err

conda activate bgmp_py310

read1="/projects/bgmp/shared/2017_sequencing/1294_S1_L008_R1_001.fastq.gz"
index1="/projects/bgmp/shared/2017_sequencing/1294_S1_L008_R2_001.fastq.gz"
index2="/projects/bgmp/shared/2017_sequencing/1294_S1_L008_R3_001.fastq.gz"
read2="/projects/bgmp/shared/2017_sequencing/1294_S1_L008_R4_001.fastq.gz"

/usr/bin/time -v ./scoreDist.py -f $read1 -o hist_read1a.png -p 101 -r 363246735
echo "DONE WITH read1"
echo ""
echo ""
/usr/bin/time -v ./scoreDist.py -f $index1 -o hist_index1a.png -p 8 -r 363246735
echo "DONE WITH index1"
echo ""
echo ""
/usr/bin/time -v ./scoreDist.py -f $index2 -o hist_index2a.png -p 8 -r 363246735
echo "DONE WITH index2"
echo ""
echo ""
/usr/bin/time -v ./scoreDist.py -f $read2 -o hist_read2a.png -p 101 -r 363246735
echo "DONE WITH read2"
echo ""
echo ""