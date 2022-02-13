#!/bin/bash -e
#SBATCH --job-name=WriteJavaFileMPI
#SBATCH --time=00:30:00
#SBATCH --ntasks=2

module load Python/3.9.5-gimkl-2020a

srun python write_java_files_from_csvs_MPI.py