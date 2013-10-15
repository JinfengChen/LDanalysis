#!/bin/bash
#PBS -l nodes=1:ppn=1
#PBS -l mem=6gb
#PBS -l walltime=100:00:00

cd $PBS_O_WORKDIR

python HaploView.py --input ../input/BGI.SNP.Jap.matrix.4 --output BGI_Jap_chr

echo "Done"
