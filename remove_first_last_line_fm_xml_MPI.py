###############################################################################
# Copy Files from source folder to subfolders inside a destination subfolders # 
###############################################################################
# Read this Post for runing processis in parallel
# https://stackoverflow.com/questions/42979271/how-to-run-multiple-instances-of-the-same-python-script-which-uses-subprocess-ca
# 
# How to use this program
# srun python remove_first_last_line_fm_xml_MPI.py -f checkstyle-result -sfd ../my_codesnippet_analysis/checkstylexmlreports_xml

# $    sbatch remove_first_last_line_fm_xml_MPI.sl



import numpy as np
import pandas as pd
from mpi4py import MPI

import subprocess as sp
# what will be used to read files
import glob
import shutil
import os
import re

import argparse

parser = argparse.ArgumentParser(
    description='Run CheckStyle on Java Apps.'
)

parser.add_argument(
     "-f",
    "--filename",
    default="",
    type=str, 
    help="Enter the name of the folders to be generated e.g., buckets will be bucket 0, 1, ..., n."
)

parser.add_argument(
     "-sfd",
    "--sourcefilrdir",
    type=str,
    help="Enter the directory to the file"
)


args = parser.parse_args()

file_name = args.filename
src_filr_dir = args.sourcefilrdir

    
#Retrieves MPI environment
comm = MPI.COMM_WORLD

#Sets size as the total number of MPI tasks
size = comm.Get_size()

#Sets rank as the specific MPI rank on all MPI tasks
rank = comm.Get_rank()


sub_file_name_array=[]
sub_file_name_array = [file_name for i in range(size)] 

#print(sub_folder_name_array[0:5])

#If the rank is 0 (master) then split filenames equally amoung size groups MPI tasks
if rank == 0:
    split_sub_file_names = np.array_split(sub_file_name_array, size, axis = 0)
    
else:
    sub_file_name_array = None
    split_sub_file_names = None
    
                                                         
#Scatter the filenames among each MPI task
rank_sub_file_name = comm.scatter(split_sub_file_names, root = 0)

####################################################################
# Perform Copy of Multiple Files from Source to Destination
###################################################################

def remove_first_last_line_fm_xml():
    
    for rank_sub_file_name in rank_sub_file_names:
        
        # derive the unique folder name of the sub folder to be created
        # comprising of the genericname and the rank number
        # e.g. bucket0, bucket1, ..., bucketn
        derive_sub_file_unique_name = '{}{}'.format(rank_sub_file_name, rank)
        
        
        fmt_cmd = 'cd {}; xmllint --format {}.xml > temp_fmt.xml | rm {}.xml | mv temp_fmt.xml {}.xml'.format(src_filr_dir, derive_sub_file_unique_name, derive_sub_file_unique_name, derive_sub_file_unique_name)
        cmd1 = sp.run(
            fmt_cmd, # command
            capture_output=True,
            text=True,
            shell=True
        )
        
        #cd src_filr_dir;
        #cd src_filr_dir; sed -i '1,2d;$d' pmd_rules_results_fmt.xml
        del_first_last_line_cmd = "cd {}; sed -i '1,2d;$d' {}".format(src_filr_dir, derive_sub_file_unique_name)
        cmd2 = sp.run(
            del_first_last_line_cmd, # command
            capture_output=True,
            text=True,
            shell=True
        )

# copy files from multiple folders to one single folder
remove_first_last_line_fm_xml()

print('Rank {} successfully copied -:)'.format(rank))




