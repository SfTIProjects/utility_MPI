#!/bin/bash -e
#SBATCH --job-name=MvFilesFmMultiSrcs
#SBATCH --time=00:10:00
#SBATCH --ntasks=201

module load Python/3.9.5-gimkl-2020a

srun python cp_files_fm_src_multi_subfolders_to_single_dst_MPI.py -ps ../my_codesnippet_analysis/CheckStyle2 -cs target -d ../my_codesnippet_analysis/CheckStyle2/checkstylexmlreports_xml -sfn my-javacodeanalysis-app -t xml -pt result -fu