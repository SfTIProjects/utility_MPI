#!/bin/bash -e
#SBATCH --job-name=WriteJavaFileMPI
#SBATCH --time=00:10:00
#SBATCH --ntasks=576 --cpus-per-task=1

module load Python/3.9.5-gimkl-2020a
srun python cp_files_fm_single_src_to_dst_multi_subfolders_MPI.py -s ../my_notebook/codesnippets_java -d ../my_notebook/temp -t java