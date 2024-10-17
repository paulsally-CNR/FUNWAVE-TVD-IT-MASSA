#!/bin/bash

# Usage: sbatch ./run_job_irr_2x2_pt.sh

# SBATCH instructions for SLURM: 
#   the job name, the proc number, and where the output and err files will be saved

##SBATCH --job-name=fw_ms_irr_30deg
#SBATCH --job-name=fw_ms_irr
#SBATCH --ntasks=28
##SBATCH --output /home/mare/funwave/output_massa/output_files/log/fw_ms_irr_30deg.%j.out
#SBATCH --output /OCEANASTORE/progetti/funwave/output_massa/output_files/log/fw_ms_irr_2x2_pt.%j.out
##SBATCH --error /home/mare/funwave/output_massa/output_files/log/fw_ms_irr_30deg.%j.err
#SBATCH --error /OCEANASTORE/progetti/funwave/output_massa/output_files/log/fw_ms_irr_2x2_pt.%j.err
#SBATCH --quiet

# source /etc/profile
source /cluster/env/C7-INT2019U3-NC473-OMPI407-AVX512.env

# Working folder
DIR="${HOME}/funwave/FUNWAVE-TVD-IT-MASSA/massa/input_files"
cd $DIR

# Inset here the process to be lunched with mpirun
# exec with mpi -
# mpirun -np 28 ./funwave--intel-parallel-single input_massa_irr30deg.txt
mpirun -np 28 ./funwave--intel-parallel-single input_massa_irr_2x2_pt.txt
