# This file implements the brute force method for the ECDH algorithm
# We want to find x such that x*G = A (mod p)

from tqdm import tqdm
import sys

from compute_sum import compute_sum

def brute_force_discrete_log(A, G, coef, p):
    max_order = int(p + 1 + 2*p**0.5)
    current_product = (None, None)
    for k in tqdm(range(1, max_order), desc = "Brute forcing", file=sys.stdout):
        current_product = compute_sum(P = current_product, Q = G, coef = coef, p = p)
        if current_product == A:
            return k

        
