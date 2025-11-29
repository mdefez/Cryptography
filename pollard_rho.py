# This file implements the phollard's rho method for the DH algorithm
# We want to find x such such as g**x [p] == A

from tqdm import tqdm
import sys
from random import randint

def compute_next_x_i(x_i, a_i, b_i, A, g, p):
    """
    Compute x_i+1, a_i+1 and b_i+1 according to x_i, a_i and b_i
    """
    if x_i % 3 == 0:
        next_x_i = pow(x_i, 2, p) 
        next_a_i = a_i * 2
        next_b_i = b_i * 2

    elif x_i % 3 == 1:
        next_x_i = (x_i * A) % p
        next_a_i = a_i
        next_b_i = b_i + 1
    
    else:
        next_x_i = (x_i * g) % p
        next_a_i = a_i + 1
        next_b_i = b_i

    return next_x_i, next_a_i, next_b_i


def find_cycle(A, g, p, nb_tries):
    """
    Compute the sequence until the p**0.6-th term, unless we find a collision first (thanks to tortoise-havre algorithm)
    It is very likely to find a collision before the sqrt(p)-th term, if we don't until the p**0.6-th term, we try again with different initialization
    """

    for run in range(nb_tries):
        a_i_tortoise = randint(1, min(100, p))
        b_i_tortoise = randint(1, min(100, p))
        values_tortoise = pow(g, a_i_tortoise, p) * pow(A, b_i_tortoise, p)

        a_i_havre = a_i_tortoise
        b_i_havre = b_i_tortoise
        values_havre = values_tortoise 

        print(f"Run {run+1}")
        for _ in tqdm(range(int(p**0.6)), desc="Looking for collision", file=sys.stdout):
            values_tortoise, a_i_tortoise, b_i_tortoise = compute_next_x_i(values_tortoise, a_i_tortoise, b_i_tortoise, A, g, p)

            values_havre, a_i_havre, b_i_havre = compute_next_x_i(values_havre, a_i_havre, b_i_havre, A, g, p)
            values_havre, a_i_havre, b_i_havre = compute_next_x_i(values_havre, a_i_havre, b_i_havre, A, g, p)

            if values_havre == values_tortoise:
                return a_i_tortoise, b_i_tortoise, a_i_havre, b_i_havre
            
    return False


# We have g**a_i * A**b_i = g**a_j * A**b_j so if we set A == g**x, we need to solve the following
# g**(a_i-a_j + x*(b_i-b_j)) = 1 mod p. Nevertheless, ord(g) = q thus, (a_i-a_j + x*(b_i-b_j)) = 0 mod(q)
# Finally, x = (a_j-a_i)*(b_i-b_j)**(-1) mod q, please note that (b_i-b_j) is inversible as q is prime so (b_i-b_j)**(-1) = (b_i-b_j)**(q-1-1) mod(q)

def solve_equation_cycle(a_i, b_i, a_j, b_j, p):
    """
    Find x out of the collision
    """
    q = (p-1) // 2
    invert_b_i_b_j = pow(b_i - b_j, q-2, q)
    x = (a_j - a_i) * invert_b_i_b_j % q 
    return x

def dh_pollard_rho(A, g, p, nb_tries = 10):
    """
    Final function that computes the key
    """
    try:
        a_i, b_i, a_j, b_j = find_cycle(A, g, p, nb_tries)
    except TypeError:
        return False 
    
    x = solve_equation_cycle(a_i, b_i, a_j, b_j, p)
    return x

