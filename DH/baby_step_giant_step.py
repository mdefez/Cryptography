# This file implements the baby step / giant step method for the DH algorithm
# We want to find x such such as g**x [p] == A

from tqdm import tqdm
import sys

def baby_step(g, p):
    n = int(p**0.5) + 1

    powers_with_exponents = {}      # Key = g**j, Value = j
    for j in tqdm(range(n), desc = "Computing baby steps", file=sys.stdout):
        powers_with_exponents[pow(g, j, p)] = j

    return powers_with_exponents

def giant_step(A, g, p):
    powers_with_exponents = baby_step(g, p)
    powers = set(powers_with_exponents.keys())

    n = int(p**0.5) + 1
    increment = pow(g, p-1-n, p)

    gamma = A 

    for i in tqdm(range(n), desc = "Computing giant steps", file=sys.stdout):
        if gamma in powers:
            j = powers_with_exponents[gamma]

            key = j + i*n
            return key
        else:
            gamma = (gamma * increment) % p

