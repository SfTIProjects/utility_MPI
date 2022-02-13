###############################################################################################
# Copy Files from Single source folder to subfolders inside a destination Multiple subfolders # 
###############################################################################################
# Read this Post for runing processis in parallel
# https://stackoverflow.com/questions/42979271/how-to-run-multiple-instances-of-the-same-python-script-which-uses-subprocess-ca
# 
# How to use this program
# srun python cp_files_fm_single_src_to_dst_multi_subfolders_MPI.py -s /path/to/folder -d dest/to/folder -t xml
# srun python cp_files_fm_single_src_to_dst_multi_subfolders_MPI.py -s ../my_notebook/codesnippets_java -d ../my_notebook/temp -t java
# To run it on slum:
# $    sbatch cp_files_fm_single_src_to_dst_multi_subfolders_MPI.sl

import numpy as np
import pandas as pd
from mpi4py import MPI

import subprocess as sp
# what will be used to read files
import glob
import shutil
import os
import re

import xml.etree.ElementTree as ET
#from xml.dom import minidom

import argparse

parser = argparse.ArgumentParser(
    description='Run CheckStyle on Java Apps.'
)

parser.add_argument(
     "-sfn",
    "--subfoldername",
    default="bucket",
    type=str, 
    help="Enter the generic name of sub folders to be generated"
)

parser.add_argument(
     "-s",
    "--src",
    type=str, 
    help="Source folder path or directory where you want to copy file to"
)

parser.add_argument(
     "-pd",
    "--parentdest",
    type=str, 
     help="The parent destination path(s) where the multiple subfolders you want to copy files to (before the autogenerated folders)"
    
)

parser.add_argument(
     "-cd",
    "--childdest",
    type=str, 
     help="The child destination path(s) where the multiple subfolders you want to copy files to (after the autogenerated folders)"
)


parser.add_argument(
     "-t",
    "--filetype",
    type=str,
    help="Enter the type of file e.g. xml, csv, txt, java, py"
)

parser.add_argument(
     "-pt",
    "--pattern",
    default="",
    type=str,
    help="Are there particular pattern of files you want to select."
)

args = parser.parse_args()

src_path = args.src
parent_dest_path = args.parentdest
child_dest_path = args.childdest
file_type = args.filetype
sub_folder_name = args.subfoldername
pattern = args.pattern


    
#Retrieves MPI environment
comm = MPI.COMM_WORLD

#Sets size as the total number of MPI tasks
size = comm.Get_size()

#Sets rank as the specific MPI rank on all MPI tasks
rank = comm.Get_rank()

# Get the directory and files
# e.g. /path/to/folder/where/files/are
# *.java
#file_location = os.path.join('/path/to/folder/where/files/are', '*.java')
file_location = os.path.join(src_folder, '{}*.{}'.format(pattern, file_type))

# get all the file names and their paths
filenames = glob.glob(file_location)

# number of files
print('Total Number of {} files: {}'.format(file_type, len(filenames)))

#If the rank is 0 (master) then split filenames equally amoung size groups MPI tasks
if rank == 0:
    split_filenames = np.array_split(filenames, size, axis = 0)
    
else:
    filenames = None
    split_filenames = None
    
                                                         
#Scatter the filenames among each MPI task
rank_filenames = comm.scatter(split_filenames, root = 0)

####################################################################
# Perform Copy of Multiple Files from Source to Destination
###################################################################

def cp_files_fm_single_src_to_dst_multi_subfolders():
    
    print('Number of {} files in this subfolder: {}'.format(file_type, len(rank_filenames)))
    
    # get unique name of a folder to be created
    # comprising of the genericname and the rank number
    # e.g. bucket0, bucket1, ..., bucketn
    unique_sub_folder_name = '{}{}'.format(sub_folder_name, rank)
    
    # create the folder
    mk_folder_cmd = 'cd {}; mkdir {}'.format(parent_dest_path, unique_sub_folder_name)
    
    if len(child_dest_path) == 0:
        mk_folder_cmd = 'cd {}; mkdir {}/{}'.format(parent_dest_path, unique_sub_folder_name, child_dest_path)
        
    cmd1 = sp.run(
        mk_folder_cmd, # command
        capture_output=True,
        text=True,
        shell=True
    )
    
    
    dest_dir = '{}/{}'.format(dest_folder, folder_name_full)
    for file in rank_filenames:
            shutil.copy(file, dest_dir)
        
    
cp_files_fm_single_src_to_dst_multi_subfolders()
print('Rank {} successfully copied -:)'.format(rank))
