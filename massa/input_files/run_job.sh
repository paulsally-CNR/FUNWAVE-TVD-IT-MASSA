#!/bin/bash

#SBATCH --ntasks 1
##SBATCH --output /OCEANASTORE/progetti/funwave/output_massa/output_files/log/fw_ms_irr_2x2_pt.%j.out
#SBATCH --output /OCEANASTORE/progetti/funwave/output_massa/output_files/log/%x.%j.out
##SBATCH --error /OCEANASTORE/progetti/funwave/output_massa/output_files/log/fw_ms_irr_2x2_pt.%j.err
#SBATCH --error /OCEANASTORE/progetti/funwave/output_massa/output_files/log/%x.%j.err
#SBATCH --quiet

# Usage: 
#   sbatch --job-name [run] --ntasks 28 ./run_job.sh
# or
#   sbatch -J [run] -n 28 ./run_job.sh
#       where [run] is the same suffix of the input file i.e. input_[run].txt

echo "Job started"

# >> Exit if run argument is missing
# if [[ $SLURM_JOB_NAME == *.sh ]]; then 
#     echo "Add option --job-name [run] (or -J) before script name: e.g. irr_2x2_pt"
#     exit 1
# else
#     echo "Job name is $SLURM_JOB_NAME"
# fi
if [[ $SLURM_JOB_NAME == *.sh ]]; then
    echo "Specify the run name: e.g. irr_2x2_pt"
    exit 1
else
    echo "Job name is $SLURM_JOB_NAME"
fi
# <<
# >> Exit if number of tasks argument is missing
if [[ -z "$SLURM_NTASKS"  || $SLURM_NTASKS -eq 1 ]]; then
    echo "Specify the number of tasks: e.g. --ntasks 28"
    exit 1
else
    echo "Number or tasks is $SLURM_NTASKS"
fi
# <<

source /cluster/env/C7-INT2019U3-NC473-OMPI407-AVX512.env

# Working folder
DIR="${HOME}/FUNWAVE/FUNWAVE-TVD-IT-MASSA/massa/input_files"
cd $DIR

# Insert here the process to be lunched with mpirun
echo "mpirun -np $SLURM_NTASKS ./funwave--intel-parallel-single input_massa_$SLURM_JOB_NAME.txt"
# mpirun -np 28 ./funwave--intel-parallel-single input_massa_irr30deg.txt
mpirun -np $SLURM_NTASKS ./funwave--intel-parallel-single input_massa_$SLURM_JOB_NAME.txt
echo "Job finished"