#!/bin/bash -e
#SBATCH --job-name=MvFilesFmMultiSrcs
#SBATCH --time=00:00:05
#SBATCH --ntasks=201

module load Python/3.9.5-gimkl-2020a

srun python remove_first_last_line_fm_xml_MPI.py -f checkstyle-result -sfd ../my_codesnippet_analysis/checkstylexmlreports_xml
