#!/bin/bash
#SBATCH --account=bgmp
#SBATCH --partition=bgmp
#SBATCH --cpus-per-task=4
#SBATCH --nodes=1
#SBATCH --time=15:00:00
#SBATCH --job-name=demultiplexer
#SBATCH --output=demultiplexer_%j.out
#SBATCH --error=demultiplexer_%j.err

conda activate bgmp_py310

knownIndex=/projects/bgmp/shared/2017_sequencing/indexes.txt
read1=/projects/bgmp/shared/2017_sequencing/1294_S1_L008_R1_001.fastq.gz
index1=/projects/bgmp/shared/2017_sequencing/1294_S1_L008_R2_001.fastq.gz
index2=/projects/bgmp/shared/2017_sequencing/1294_S1_L008_R3_001.fastq.gz
read2=/projects/bgmp/shared/2017_sequencing/1294_S1_L008_R4_001.fastq.gz

/usr/bin/time -v ./demultiplexer.py \
    -k $knownIndex \
    -r1 $read1 \
    -i1 $index1 \
    -i2 $index2 \
    -r2 $read2 \
    -n 363246735
echo "DONE"

# srun --account=bgmp --partition=bgmp --nodes=1 --time=2:00:00 --cpus-per-task=20 --pty bash
# /usr/bin/time -v pigz *.fq