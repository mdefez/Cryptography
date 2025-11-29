# In this file we will implement a method to simulate a Diffie-Hellmann key exchange
# Then we will test different methods to force the key

import random
from time import time
from functools import partial

# We will use 3 examples of safe primes, p2, p12 and p16. The number corresponds to the numer of digits
# The generator will be g = 4, this way ord(g) = (p-1) / 2
# p2 = 23; p12 = 324_528_684_947; p16 = 1_000_000_000_005_719
p = 1_000_000_000_005_719
g = 4


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
        self.A = pow(g, self.a, p)
    
    def compute_key(self, B):
        self.key = pow(B, self.a, p)

# Bob has the same features as Alice
class Bob:
    def choose_b(self, min = 1, max = p-1):
        self.b = random.randint(min, max)
    
    def generate_B(self):
        self.B = pow(g, self.b, p)
    
    def compute_key(self, A):
        self.key = pow(A, self.b, p)

def simulate_nego():
    """
    Simulate a DH key exchange
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
    for _ in range(100):
        key_alice, key_bob = simulate_nego()
        assert key_alice == key_bob



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
    method should take A, g, p as arguments and return the solution x if found, else False
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
    a_rogue = method(A = alice.A, g = g, p = p)
    if a_rogue == False:
        print("No solutions found")
        return False

    key_rogue = pow(bob.B, a_rogue, p)

    alice.compute_key(bob.B)
    
    assert key_rogue == alice.key

############################################################## Brute force method ############################################################################################################################
from brute_force import brute_force_discrete_log

# Takes approx 200 hours for p12

# Uncomment here
# compute_key(brute_force_discrete_log, "Brute-force")

############################################################## Little step giant step method ############################################################################################################################
from baby_step_giant_step import giant_step

# Takes a few seconds for p12, a few minutes for p16

# Uncomment here
# compute_key(giant_step, "Baby step / Giant step")

############################################################## Little step giant step method ############################################################################################################################
from pollard_rho import dh_pollard_rho

# Takes a few seconds for p12, 1 hour for p16

# Uncomment here
# compute_key(partial(dh_pollard_rho, nb_tries=3), "Pollard rho")

