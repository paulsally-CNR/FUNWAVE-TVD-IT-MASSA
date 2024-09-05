#!/bin/bash

# Usage: sbatch ./run_slurm_funwave.sh

#SBATH instruction for SLURM: the job name, the proc number, and where the lo and err files will be saved
#SBATCH --job-name=input_massa_2x2_pt
#SBATCH --ntasks=28
#SBATCH -o /home/mare/funwave/output_massa/output_files/massa_2x2_%j.out
#SBATCH -e /home/mare/funwave/output_massa/output_files/massa_2x2_%j.err
#SBATCH -Q

source /etc/profile
source /cluster/env/C7-INT2019U3-NC473-OMPI407-AVX512.env


#Insert working folder here
DIR="${HOME}/funwave/FUNWAVE-TVD/massa/input_files"

cd $DIR


#Inset here the process to be lunched with mpirun
#exec with mpi -
mpirun -np 28 ./funwave--intel-parallel-single input_massa_2x2_pt.txt



