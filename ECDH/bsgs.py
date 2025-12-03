# This file implements the baby step / giant step method for the ECDH algorithm
# We want to find x such such as x*G = A (mod p)

from tqdm import tqdm
import sys
from compute_sum import compute_sum, compute_homothety

def baby_step(G, p, coef):
    n = int(p**0.5) + 1

    multiples_with_exponents = {}      # Key = j*G, Value = j
    current_multiple = (None, None)
    for j in tqdm(range(1, n), desc = "Computing baby steps", file=sys.stdout):
        current_multiple = compute_sum(P = current_multiple, Q = G, p = p, coef = coef)
        multiples_with_exponents[current_multiple] = j

    return multiples_with_exponents

def giant_step(A, G, coef, p):
    multiples_with_exponents = baby_step(G, p, coef)
    multiples = set(multiples_with_exponents.keys())

    n = int(p**0.5) + 1
    increment = compute_homothety(X=G, k=n, coef=coef, p = p)
    x, y = increment 
    inv_y = (-y) % p
    inv_increment = (x, inv_y)

    gamma = A 

    for i in tqdm(range(n), desc = "Computing giant steps", file=sys.stdout):
        if gamma in multiples:
            j = multiples_with_exponents[gamma]

            key = j + i*n
            return key
        else:
            gamma = compute_sum(P = gamma, Q = inv_increment, p = p, coef=coef)

