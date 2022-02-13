#https://support.nesi.org.nz/hc/en-gb/articles/360001173875-MPI-Scaling-Example
#Imports numpy and mpi4py
import numpy as np
from mpi4py import MPI

# what will be used to read files
import glob
import os
import pandas as pd

#Retrieves MPI environment
comm = MPI.COMM_WORLD

#Sets size as the total number of MPI tasks
size = comm.Get_size()

#Sets rank as the specific MPI rank on all MPI tasks
rank = comm.Get_rank()

# Get the directory of all the files to be read from
# get the directory to where the *.csv files in the pmdpasscodesnippets_csv path or folder
file_location = os.path.join('pmdpasscodesnippets_csv', '*.csv')

# get all the file names and their paths
filenames = glob.glob(file_location)


# number of files
print('Number of Java Files {}'.format(len(filenames)))


#If the rank is 0 (master) then split filenames equally amoung size groups MPI tasks
if rank == 0:
    split_filenames = np.array_split(filenames, size, axis = 0)
else:
    filenames = None
    split_filenames = None
    
#Scatter the filenames among each MPI task
rank_filenames = comm.scatter(split_filenames, root = 0)

########################################################
# Working on multiple dataframes returned by each rank #
########################################################
#https://jonathansoma.com/lede/foundations-2017/classes/working-with-many-files/class/

#Step1: Turn the list of filenames (rank_filenames) into a list of dataframes
#list_of_dfs = [pd.read_csv(filename) for filename in filenames]
list_of_dfs = [pd.read_csv(filename) for filename in rank_filenames]

#Step2: Add the filename to each dataframe
# zip loops through TWO THINGS AT ONCE
# so you're looking at dataframe #1 and filename #1
# then dataframe #2 and filename #2
# etc
# and assigning that filename (rank_filenames) as a new column in the dataframe
for df, filename in zip(list_of_dfs, rank_filenames):
  df['filename'] = filename
    
#Step3: Combine multiple dataframes
# Combine a list of dataframes, on top of each other
combined_df = pd.concat(list_of_dfs, ignore_index=True)

    
# Read the Idx match and Code column on the combined_df and
# write as a .java File into the pmdpasscodesnippets_java directory
for index, row in combined_df.iterrows():
    #open('javaclasses/Code'+str(index)+'_'+str(row['Idx'])+'_'+str(row['match'])+'.java', 'w').write(row['Code'])
    open('pmdpasscodesnippets_java/Code'+'_'+str(row['Idx'])+'_'+str(row['match'])+'.java', 'w').write(row['Code'])
    
# There is no need for a gather here
# data_gather = comm.gather(...)
