# import libraries
from mpi4py import MPI   # import MPI
import generate_frame

# get the 'communicator'
comm = MPI.COMM_WORLD

# get the 'rank' of the process
my_rank = comm.rank   # this differs between copies of the program

# get the total number of processes
total_ranks = comm.size   # number of copies running

total_work = 720
# get the amount of work per worker
work_per_worker = total_work/total_ranks

# set the start and end indices for the each rank
start_idx = int(my_rank * work_per_worker)
end_idx = int((my_rank+1) * work_per_worker - 1)

print(f"rank {my_rank}/{total_ranks}: [{start_idx}...{end_idx}]")

for i in range(start_idx, end_idx+1):
    print(f"rank {my_rank}/{total_ranks}: working on {i}")
    generate_frame.generate_frame(i)