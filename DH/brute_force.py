# This file implements the brute force method for the DH algorithm
# We want to find x such such as g**x [p] == A

from tqdm import tqdm
import sys

def brute_force_discrete_log(A, g, p):
    current_power = 1
    for k in tqdm(range(1, p), desc = "Brute forcing", file=sys.stdout):
        current_power = (current_power * g) % p 
        if current_power == A:
            return k

        
