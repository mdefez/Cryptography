# In this file we will implement a method to simulate a Elliptic-Curve-Diffie-Hellmann key exchange
# Then we will test different methods to force the key

import random
from time import time
from functools import partial

# Function to computes the sum of shape k*X (mod p)
from compute_sum import compute_homothety

# In the whole file we will name (None, None) the infinity point

############################################# Example of curves, prime and generators #########################################################################################

# First example
# C : y**2 ≡ x**3 + 2x + 2 mod(p)
# coef = 2       # Term in front of x
# p = 17
# G = (5, 1)      

# Second example
# C : y**2 ≡ x**3 - x + 1 mod(p)
coef = -1       # Term in front of x
p = 324_528_684_947
G = (0, 1) 

# Third example
# C : y**2 ≡ x**3 + x + 6 mod(p)
# coef = 1       # Term in front of x
# p = 1_000_000_000_005_719
# G = (2, 4)     

class Alice:
    """
    Create a class that allows to simulate Alice's role by choosing a and computing both A and key (thanks to B)
    """
    def choose_a(self, a = False, min = 1, max = p-1):
        if a:
            self.a = a
        else:
            self.a = random.randint(min, max)
    
    def generate_A(self):
        self.A = compute_homothety(X = G, k=self.a, coef = coef, p = p)
    
    def compute_key(self, B):
        self.key = compute_homothety(X = B, k=self.a, coef = coef, p = p)

# Bob has the same features as Alice
class Bob:
    def choose_b(self, min = 1, max = p-1):
        self.b = random.randint(min, max)
    
    def generate_B(self):
        self.B = compute_homothety(X = G, k=self.b, coef = coef, p = p)
    
    def compute_key(self, A):
        self.key = compute_homothety(X = A, k=self.b, coef = coef, p = p)

def simulate_nego():
    """
    Simulate a ECDH key exchange
    """
    alice = Alice() 
    alice.choose_a()
    alice.generate_A()

    bob = Bob()
    bob.choose_b()
    bob.generate_B()

    alice.compute_key(bob.B)
    bob.compute_key(alice.A)

    return alice.key, bob.key

# Test if both agents compute the same key
def test_nego():
    for _ in range(10):
        key_alice, key_bob = simulate_nego()

        assert key_alice == key_bob

# It passes
# test_nego()

def computing_time(func):
    """
    Decorator used to compute the time needed to force the key
    """
    def wrapper(*args):
        start = time()
        func(*args)
        end = time()
        print(f"Computing time : {round(end - start, 4)} seconds")
    return wrapper


# Generic function to test any method
@computing_time
def compute_key(method, name_method):    
    """
    The goal is to find x where xG = A (mod p)
    method should take A, G, coef and p as arguments and return the solution x if found, else False
    name_method is a the name of the method represented as a string.

    Keep in mind we use tqdm to vizualize progression but by no means one need to reach 100% to find the key as it is randomly distributed in [1, p]
    """

    alice = Alice() 
    alice.choose_a()
    alice.generate_A()

    bob = Bob()
    bob.choose_b()
    bob.generate_B()

    print(f"Starting to force the key with method : {name_method}")
    a_rogue = method(A = alice.A, G = G, coef = coef, p = p)
    if a_rogue == False:
        print("No solutions found")
        return False

    key_rogue = compute_homothety(X = bob.B, k=a_rogue, coef = coef, p = p)

    alice.compute_key(bob.B)
    
    assert key_rogue == alice.key

############################################################## Brute force method ############################################################################################################################
from brute_force import brute_force_discrete_log

# compute_key(brute_force_discrete_log, "Brute Force")

############################################################## Little step giant step method ############################################################################################################################
from bsgs import giant_step

compute_key(giant_step, "Baby steps Giant steps")

############################################################## Pollard's rho method ############################################################################################################################


