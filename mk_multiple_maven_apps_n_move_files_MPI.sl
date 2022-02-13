#!/bin/bash -e
#SBATCH --job-name=WriteJavaFileMPI
#SBATCH --time=00:10:00
#SBATCH --ntasks=201 --cpus-per-task=1

module load Maven/3.6.0
module load Python/3.9.5-gimkl-2020a
srun python mk_multiple_maven_apps_n_move_files_MPI.py -s ../pmdpasscodesnippets_java -pd ../my_codesnippet_analysis/CheckStyle3 -csp checks_lib -r