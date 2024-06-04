# import libraries
from mpi4py import MPI   # import MPI

# get the 'communicator'
comm = MPI.COMM_WORLD

# get the 'rank' of the process
my_rank = comm.rank   # this differs between copies of the program

# get the total number of processes
total_ranks = comm.size   # number of copies running

# print the rank
print(f"I am {my_rank} of {total_ranks}. I am borg.")

#*******************************************************************************
# Once the code has been drafted and tested, follow the instructions in the
# following URL to test your code in parallel:
# https://github.com/taobrienlbl/advanced_earth_science_data_analysis/blob/spring_2023_iub/lessons/09_parallelization_intro/09_workalong_01_instructions.md
#*******************************************************************************