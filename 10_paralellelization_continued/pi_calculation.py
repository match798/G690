""" This cell calculates pi via the Madhava-Leibniz series: https://en.wikipedia.org/wiki/Approximations_of_%CF%80#Middle_Ages """

#import MPI
from mpi4py import MPI
import numpy as np

# get the communicator
comm = MPI.COMM_WORLD
# get the mpi rank
rank =  comm.rank

# set the number of terms in the sum
terms_per_rank = int(1e7)

# set the indices for this rank
start_idx = rank * terms_per_rank + 1
end_idx = (rank + 1) * terms_per_rank + 1

# initialize pi to 0
pi_part = 0

# loop over the terms
for n in range(start_idx, end_idx):
    if n == 1:
        term = 1
    else:
        term = -((-1)**n) / (2*n - 1)
    pi_part += term

# sum the results across all ranks by gathering the results on rank 0
pi_parts = comm.gather(pi_part, root=0)
pi = 4*sum(pi_parts)

# print 100 digits of pi
if rank == 0:
    print(f"pi    = {pi}")
    print(f"np.pi = {np.pi}")