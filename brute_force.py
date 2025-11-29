# This file implements the brute force method for the DH algorithm
# We want to find x such such as g**x [p] == A

from tqdm import tqdm
import sys

def brute_force_discrete_log(A, g, p):
    for k in tqdm(range(p), desc = "Brute forcing", file=sys.stdout):
        if pow(g, k, p) == A:
            return k

        
