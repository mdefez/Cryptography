# The goal of this file is to compute k*G, we do it in 3 parts

# First step : Define a function that computes 2*G
# Second step : Define a function that compute P + Q (when P != Q)
# Last step : Write k with the binary decomposition and compute sum_i k_i * (2**i * G) with the first 2 functions

# Compute 2*X
def compute_double(X, coef, p):
    x, y = X
    if y == 0:
        return (None, None)

    inverse_2y = pow(2*y, p-2, p)
    slope = ((3*x**2 + coef) * inverse_2y) % p
    new_x = (pow(slope, 2, p) - 2*x) % p
    new_y = (slope*(x-new_x) - y) % p

    return (new_x, new_y)

# Compute the sum between P and Q 
def compute_sum(P, Q, p, coef= None):
    x1, y1 = P
    x2, y2 = Q 

    # Deal with edge cases
    if (x1, y1) == (None, None):
        return Q 
    if (x2, y2) == (None, None):
        return P 
    if P == Q:
        return compute_double(P, coef, p)
    if x1 == x2 and (y1 + y2) % p == 0:
        return (None, None)


    inv_x2_x1 = pow(x2-x1, p-2, p)
    slope = ((y2 - y1) * inv_x2_x1) % p 

    new_x = (pow(slope, 2, p) - x1 - x2) % p
    new_y = (slope * (x1 - new_x) - y1) % p

    return (new_x, new_y)

# Computes kG
def compute_homothety(X, k, coef, p):
    binary = bin(k)
    sum = (None, None)
    current_power = X

    for i in reversed(binary):
        if i == "b":
            break
        if i == "1":
            sum = compute_sum(sum, current_power, p, coef=coef)
        
        current_power = compute_double(current_power, coef, p)

    return sum

